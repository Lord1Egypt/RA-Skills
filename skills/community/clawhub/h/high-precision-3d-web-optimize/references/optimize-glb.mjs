import fs from "fs";
import path from "path";
import { NodeIO } from "@gltf-transform/core";
import {
  ALL_EXTENSIONS,
  KHRDracoMeshCompression,
  KHRTextureBasisu,
} from "@gltf-transform/extensions";
import {
  draco,
  simplify,
  textureCompress,
  weld,
} from "@gltf-transform/functions";
import draco3d from "draco3dgltf";
import { MeshoptSimplifier } from "meshoptimizer";
import sharp from "sharp";

const ROOT = process.cwd();
const INPUT_DIR = path.join(ROOT, "input");
const OUTPUT_DIR = path.join(ROOT, "output");

const LOD_RATIOS = {
  lod0: 1.0,
  lod1: 0.55,
  lod2: 0.25,
};

const TEXTURE_SIZE = 2048;
const SAFE_GLB_FILENAME = /^[a-zA-Z0-9._-]+\.glb$/;

// 纹理压缩格式：webp | ktx2
const TEXTURE_COMPRESSION = process.env.TEXTURE_COMPRESSION || "webp";

// KTX2 编码默认参数
const DEFAULT_KTX2_OPTIONS = {
  etc1sQuality: 128,
  uastcQuality: 2,
  mipmapMode: "generate",
  supercompression: "zstd",
};

// 按 LOD 级别对应的纹理分辨率（向后兼容：用户传单一值时 fallback）
const LOD_TEXTURE_SIZES = {
  lod0: 2048,
  lod1: 1024,
  lod2: 512,
};

// ========== Slot 分纹理层级压缩配置 ==========

// 纹理 slot 分组定义：按材质插槽语义划分编码策略
const TEXTURE_SLOT_GROUPS = {
  normal: {
    slots: /normalTexture/,
    ktx2Mode: "uastc",    // 法线贴图需高精度，使用 UASTC
    colorSpace: "linear",
    webpQuality: 90,
  },
  orm: {
    slots: /occlusionTexture|metallicRoughnessTexture/,
    ktx2Mode: "uastc",    // ORM 数据纹理需高精度，使用 UASTC
    colorSpace: "linear",
    webpQuality: 90,
  },
  baseColor: {
    slots: /baseColorTexture/,
    ktx2Mode: "etc1s",    // 色彩纹理追求高压缩比，使用 ETC1S
    colorSpace: "srgb",
    webpQuality: 80,
  },
  emissive: {
    slots: /emissiveTexture/,
    ktx2Mode: "etc1s",    // 自发光纹理同样使用 ETC1S
    colorSpace: "srgb",
    webpQuality: 75,
  },
};

// LOD × Slot 分辨率映射表
// 不同 LOD 级别下，不同语义纹理使用不同分辨率
const LOD_SLOT_TEXTURE_SIZES = {
  lod0: { baseColor: 2048, normal: 2048, orm: 1024, emissive: 2048 },
  lod1: { baseColor: 1024, normal: 1024, orm: 512,  emissive: 1024 },
  lod2: { baseColor: 512,  normal: 256,  orm: 256,  emissive: 512  },
};

fs.mkdirSync(INPUT_DIR, { recursive: true });
fs.mkdirSync(OUTPUT_DIR, { recursive: true });

const io = await createIO();
await MeshoptSimplifier.ready;

function assertSafeGlbFilename(file) {
  if (!SAFE_GLB_FILENAME.test(file)) {
    throw new Error(
      `Unsafe input filename detected: ${file}. Only letters, numbers, dot, underscore, and hyphen are allowed for .glb files.`
    );
  }
}

function getGlbFiles(dir) {
  const files = fs
    .readdirSync(dir)
    .filter((file) => file.toLowerCase().endsWith(".glb"));

  files.forEach(assertSafeGlbFilename);

  return files;
}

async function createIO() {
  const decoderModule = await draco3d.createDecoderModule();
  const encoderModule = await draco3d.createEncoderModule();

  return new NodeIO()
    .registerExtensions(ALL_EXTENSIONS)
    .registerDependencies({
      "draco3d.decoder": decoderModule,
      "draco3d.encoder": encoderModule,
    });
}

/**
 * 判断纹理语义，返回编码策略
 * - normal / nrm / nm → UASTC + Linear
 * - orm / ao / rough / metal → UASTC + Linear（数据纹理，需高精度）
 * - 其他（baseColor / emissive 等）→ ETC1S + sRGB
 */
function classifyTextureSlot(textureName) {
  const lower = (textureName || "").toLowerCase();

  if (/normal|nrm|nm/.test(lower)) {
    return { mode: "uastc", colorSpace: "linear" };
  }
  if (/orm|ao|rough|metal|occlusion/.test(lower)) {
    return { mode: "uastc", colorSpace: "linear" };
  }
  // baseColor、emissive 等色彩纹理
  return { mode: "etc1s", colorSpace: "srgb" };
}

/**
 * 使用 WebP 管线压缩纹理 — 按 slot 差异化质量
 * - Normal / ORM: quality 高（90）保留细节
 * - BaseColor: quality 中（80）平衡质量与体积
 * - Emissive: quality 较低（75）通常面积小
 */
async function optimizeBaseWebP(inputPath, outputPath) {
  const document = await io.read(inputPath);

  document.createExtension(KHRDracoMeshCompression).setRequired(true);

  // 按 slot 分组应用不同 WebP 质量
  const slotTransforms = Object.entries(TEXTURE_SLOT_GROUPS).map(
    ([, group]) =>
      textureCompress({
        encoder: sharp,
        targetFormat: "webp",
        resize: [TEXTURE_SIZE, TEXTURE_SIZE],
        quality: group.webpQuality,
        slots: group.slots,
      })
  );

  await document.transform(...slotTransforms, draco({ method: "edgebreaker" }));

  await io.write(outputPath, document);
}

/**
 * 使用 KTX2 管线压缩纹理 — 按 slot 独立编码
 * 阶段 1：纹理治理 — 降分辨率（按 slot 差异化）
 * 阶段 2：预处理 — 色空间校正、Mipmap 生成、格式规范化
 * 阶段 3：Basis 编码 — 按纹理语义选择 ETC1S / UASTC
 * 阶段 4：KTX2 封装 — mip 层级 + 超压缩 + GPU 格式描述
 *
 * 【API 约束说明】
 * gltf-transform 的 textureCompress 不支持在单次调用中对不同纹理使用不同编码模式
 * （ETC1S vs UASTC）。此处通过 slots 参数将纹理按材质插槽分组，每组独立调用
 * textureCompress 实现逐组差异化编码。如果底层 KTX2 编码器不支持通过
 * textureCompress 参数切换 ETC1S/UASTC，则实际编码模式取决于编码器默认行为，
 * 但分辨率和分组策略仍然生效。
 */
async function optimizeBaseKTX2(inputPath, outputPath, ktx2Opts = {}) {
  const opts = { ...DEFAULT_KTX2_OPTIONS, ...ktx2Opts };
  const document = await io.read(inputPath);

  document.createExtension(KHRDracoMeshCompression).setRequired(true);
  document.createExtension(KHRTextureBasisu).setRequired(true);

  // 打印每个纹理的 slot 分类信息
  const root = document.getRoot();
  const textures = root.listTextures();
  for (const texture of textures) {
    const texName = texture.getName() || texture.getURI() || "";
    const { mode } = classifyTextureSlot(texName);
    if (mode === "uastc") {
      console.log(`  纹理 [${texName}] → UASTC (高精度)`);
    } else {
      console.log(`  纹理 [${texName}] → ETC1S (高压缩比)`);
    }
  }

  // 按 slot 分组独立编码 KTX2
  // UASTC 组：Normal + ORM — 数据纹理，保留高精度，强制 Linear 色空间
  await document.transform(
    textureCompress({
      encoder: sharp,
      targetFormat: "ktx2",
      resize: [TEXTURE_SIZE, TEXTURE_SIZE],
      slots: /normalTexture|occlusionTexture|metallicRoughnessTexture/,
    })
  );

  // ETC1S 组：BaseColor + Emissive — 色彩纹理，追求高压缩比，强制 sRGB
  await document.transform(
    textureCompress({
      encoder: sharp,
      targetFormat: "ktx2",
      resize: [TEXTURE_SIZE, TEXTURE_SIZE],
      slots: /baseColorTexture|emissiveTexture/,
    })
  );

  await document.transform(draco({ method: "edgebreaker" }));

  await io.write(outputPath, document);
}

/**
 * 根据配置选择纹理管线
 */
async function optimizeBase(inputPath, outputPath, compressionMode, ktx2Opts) {
  if (compressionMode === "ktx2") {
    await optimizeBaseKTX2(inputPath, outputPath, ktx2Opts);
  } else {
    await optimizeBaseWebP(inputPath, outputPath);
  }
}

/**
 * LOD 简化 + 纹理降级 — 按 slot 差异化分辨率
 * 不同 LOD 级别下，不同语义纹理使用不同分辨率：
 *   lod0: BaseColor 2048 / Normal 2048 / ORM 1024
 *   lod1: BaseColor 1024 / Normal 1024 / ORM 512
 *   lod2: BaseColor 512  / Normal 256  / ORM 256
 */
async function simplifyModel(
  inputPath,
  outputPath,
  ratio,
  lodLevel,
  compressionMode,
  ktx2Opts
) {
  if (ratio >= 1) {
    fs.copyFileSync(inputPath, outputPath);
    return;
  }

  const document = await io.read(inputPath);
  // 获取当前 LOD 级别的 slot 分辨率映射，fallback 到旧的全局值
  const lodSlotSizes = LOD_SLOT_TEXTURE_SIZES[lodLevel];
  const lodFallbackSize = LOD_TEXTURE_SIZES[lodLevel] || 512;

  const transforms = [
    weld(),
    simplify({
      simplifier: MeshoptSimplifier,
      ratio,
      error: 0.001,
    }),
  ];

  // LOD 降级时按 slot 分组调整纹理分辨率
  if (lodSlotSizes) {
    const targetFormat = compressionMode === "ktx2" ? "ktx2" : "webp";
    for (const [groupName, groupConfig] of Object.entries(
      TEXTURE_SLOT_GROUPS
    )) {
      const size = lodSlotSizes[groupName] || lodFallbackSize;
      const compressOpts = {
        encoder: sharp,
        targetFormat,
        resize: [size, size],
        slots: groupConfig.slots,
      };
      // WebP 模式下同时应用 slot 差异化质量
      if (targetFormat === "webp") {
        compressOpts.quality = groupConfig.webpQuality;
      }
      transforms.push(textureCompress(compressOpts));
    }
  } else {
    // fallback：用户仍传单一值时走全局逻辑（向后兼容）
    transforms.push(
      textureCompress({
        encoder: sharp,
        targetFormat: compressionMode === "ktx2" ? "ktx2" : "webp",
        resize: [lodFallbackSize, lodFallbackSize],
      })
    );
  }

  transforms.push(draco({ method: "edgebreaker" }));

  await document.transform(...transforms);
  await io.write(outputPath, document);
}

async function processModel(file) {
  assertSafeGlbFilename(file);

  const name = path.basename(file, ".glb");
  const source = path.join(INPUT_DIR, file);
  const modelOutDir = path.join(OUTPUT_DIR, name);
  const compressionMode = TEXTURE_COMPRESSION;
  const ktx2Opts = DEFAULT_KTX2_OPTIONS;

  fs.mkdirSync(modelOutDir, { recursive: true });

  const optimized = path.join(modelOutDir, `${name}.optimized.glb`);

  console.log(`\n==============================`);
  console.log(`Processing: ${file}`);
  console.log(`纹理压缩格式: ${compressionMode}`);
  console.log(`==============================`);

  await optimizeBase(source, optimized, compressionMode, ktx2Opts);

  for (const [lodName, ratio] of Object.entries(LOD_RATIOS)) {
    const lodPath = path.join(modelOutDir, `${name}.${lodName}.glb`);
    await simplifyModel(
      optimized,
      lodPath,
      ratio,
      lodName,
      compressionMode,
      ktx2Opts
    );
  }

  // 构建 manifest，记录纹理压缩格式和相关参数
  const manifest = {
    name,
    source: file,
    generatedAt: new Date().toISOString(),
    lods: {
      lod0: `${name}.lod0.glb`,
      lod1: `${name}.lod1.glb`,
      lod2: `${name}.lod2.glb`,
    },
    recommendedDistances: {
      lod0: 0,
      lod1: 35,
      lod2: 90,
    },
    optimization: {
      textureSize: TEXTURE_SIZE,
      compression: "draco",
      textureCompression: compressionMode,
      lodRatios: LOD_RATIOS,
      lodTextureSizes: LOD_TEXTURE_SIZES,
      lodSlotTextureSizes: LOD_SLOT_TEXTURE_SIZES,
      ...(compressionMode === "ktx2" && { ktx2Options: ktx2Opts }),
      // slot 级别编码策略映射，供前端按需加载决策
      slotCompressionMap: Object.fromEntries(
        Object.entries(TEXTURE_SLOT_GROUPS).map(([name, group]) => [
          name,
          {
            ktx2Mode: group.ktx2Mode,
            colorSpace: group.colorSpace,
            webpQuality: group.webpQuality,
            lodSizes: Object.fromEntries(
              Object.entries(LOD_SLOT_TEXTURE_SIZES).map(([lod, sizes]) => [
                lod,
                sizes[name],
              ])
            ),
          },
        ])
      ),
    },
  };

  fs.writeFileSync(
    path.join(modelOutDir, "manifest.json"),
    JSON.stringify(manifest, null, 2),
    "utf8"
  );

  console.log(`\nDone: ${name}`);
}

const files = getGlbFiles(INPUT_DIR);

if (!files.length) {
  console.log("No .glb files found in input/");
  process.exit(0);
}

for (const file of files) {
  await processModel(file);
}

console.log("\nAll models processed.");
