---
name: high-precision-3d-web-optimize
description: Optimize high-precision .glb/.gltf models for Web 3D and digital twin delivery. Use when preparing Three.js or Babylon.js assets that need UV-safe simplification, slot-based texture compression (Normal/ORM → UASTC, BaseColor/Emissive → ETC1S), differentiated LOD × slot resolution, Draco compression, LOD generation, manifest outputs, and browser-friendly loading performance without breaking UVs, materials, or texture appearance. Avoid destructive remesh or re-topology unless the user explicitly requests editable low-poly assets.
---

# High-Precision 3D Web Optimize

将高精度 GLB/GLTF 模型优化为适合 Web 3D 与数字孪生平台交付的轻量化资产，重点是 **保护 UV、保护材质与贴图表现、降低文件体积与浏览器渲染压力，并输出可直接接入的 LOD 结果**。

## Do this by default

1. 先判断模型是否属于高精度交付资产，是否存在高面数、高贴图成本或不规则拓扑风险。
2. 默认保持 workflow UV-safe。
3. 优先做 geometry / texture optimization，再考虑 retopo。
4. 生成 `optimized.glb`、`lod0.glb`、`lod1.glb`、`lod2.glb` 和 `manifest.json`。
5. 在 Three.js 或 Babylon.js 中验证加载结果。

## Recommended workflow

1. 检查 model origin、UV risk、topology risk
2. 清理 invalid / dirty geometry
3. **选择纹理压缩格式**：
   - **WebP**（默认）：浏览器原生支持、工具链简单、适合大多数 Web 场景
   - **KTX2**：GPU 原生纹理、零 CPU 解码开销、适合重度 3D 场景（大量模型同屏、移动端 GPU 受限、需要 Mipmap 精确控制）
4. 执行 UV-safe simplification
5. 压缩 textures and geometry（按 slot 分层选择编码策略与质量参数）
6. 生成 `lod0`、`lod1`、`lod2`（按 LOD 级别对不同 slot 差异化分辨率与编码）
7. 写出 `manifest.json`（含纹理格式、KTX2 参数、slot 级别压缩映射）
8. 验证 browser loading、Draco 解码、KTX2 解码（如适用）与 LOD switching
9. 根据结果给出 tuning advice

## Treat as high-precision optimization candidates when you see

- messy UVs / UV 混乱
- noisy surfaces / 表面噪声重
- baked-looking shadows / 带明显烘焙阴影
- irregular topology / 拓扑不规则
- unusually high polygon count / 面数异常高
- abnormally large `.glb` size / 文件体积异常大
- high texture resolution or heavy material stacks / 高分辨率贴图或重材质栈

## Avoid by default

- Voxel Remesh
- Quad Remesh
- destructive re-topology that reuses original textures without rebake
- workflows likely to break UV alignment
- 无 Bake 的破坏性重拓扑复材质流程

## Default outputs

```text
output/
└─ model-name/
   ├─ model-name.optimized.glb
   ├─ model-name.lod0.glb
   ├─ model-name.lod1.glb
   ├─ model-name.lod2.glb
   └─ manifest.json
```

## Default parameters

```json
{
  "lod0": 1.0,
  "lod1": 0.55,
  "lod2": 0.25,
  "textureSize": 2048,
  "geometryCompression": "draco",
  "textureCompression": "webp",
  "ktx2Options": {
    "etc1sQuality": 128,
    "uastcQuality": 2,
    "mipmapMode": "generate",
    "supercompression": "zstd"
  },
  "textureSlotGroups": {
    "normal": { "ktx2Mode": "uastc", "colorSpace": "linear", "webpQuality": 90 },
    "orm": { "ktx2Mode": "uastc", "colorSpace": "linear", "webpQuality": 90 },
    "baseColor": { "ktx2Mode": "etc1s", "colorSpace": "srgb", "webpQuality": 80 },
    "emissive": { "ktx2Mode": "etc1s", "colorSpace": "srgb", "webpQuality": 75 }
  },
  "lodSlotTextureSizes": {
    "lod0": { "baseColor": 2048, "normal": 2048, "orm": 1024, "emissive": 2048 },
    "lod1": { "baseColor": 1024, "normal": 1024, "orm": 512,  "emissive": 1024 },
    "lod2": { "baseColor": 512,  "normal": 256,  "orm": 256,  "emissive": 512  }
  }
}
```

- `textureCompression`：`"webp"` | `"ktx2"`，默认 `"webp"`。
- `ktx2Options`：仅在 `textureCompression === "ktx2"` 时生效。
- `textureSlotGroups`：定义每个纹理 slot 的编码策略（KTX2 模式 / 色空间 / WebP 质量）。
- `lodSlotTextureSizes`：LOD 级别 × slot 的差异化分辨率映射，远景 slot 可更激进降级。

## Slot-Based Texture Compression / Slot 分纹理层级压缩

Applying identical compression to all textures either bloats size (over-preserving unimportant slots) or over-compresses critical slots. Slot-based logic differentiates by texture semantics:

| Slot | KTX2 Mode | Color Space | WebP Quality | Notes |
| ---- | --------- | ----------- | ------------- | ----- |
| Normal | UASTC | Linear | 90 | Normal maps are precision-sensitive; block artifacts cause lighting jitter |
| ORM | UASTC | Linear | 90 | Data textures; channel precision affects material appearance |
| BaseColor | ETC1S | sRGB | 80 | Color textures tolerate compression; high ratio preferred |
| Emissive | ETC1S | sRGB | 75 | Usually small area; can compress more aggressively |

**LOD × Slot resolution / LOD × Slot 分辨率映射：**

| LOD | BaseColor | Normal | ORM | Emissive |
| --- | --------- | ------ | --- | -------- |
| lod0 | 2048 | 2048 | 1024 | 2048 |
| lod1 | 1024 | 1024 | 512 | 1024 |
| lod2 | 512 | 256 | 256 | 512 |

Front-end loaders can read `slotCompressionMap` from `manifest.json` to make per-slot lazy-loading decisions.

### API Constraint / API 约束

gltf-transform `textureCompress` does not support switching ETC1S/UASTC per texture in a single call. The current implementation works around this by grouping textures via the `slots` parameter and calling `textureCompress` separately per group. Once gltf-transform adds a `mode` parameter, per-texture encoding can be controlled more precisely.

## Suggested targets

| Metric | Recommended value |
| --- | ---: |
| Single model size | < 10 MB |
| Mobile single model size | < 5 MB |
| Single model triangle budget | < 100k |
| Main scene total triangle budget | < 2M |
| First screen load time | < 3 s |

## Troubleshooting

### Material looks blurry / 材质变糊
- raise `textureSize`，如 `1024 -> 2048`
- reduce texture compression strength
- preserve more geometry in `lod0`

### Model is still too large / 模型仍然太大
- reduce texture size
- make `lod1` and `lod2` more aggressive
- confirm Draco or Meshopt is enabled
- split the asset for lazy loading if needed

### Model deforms after simplification / 模型变形或破面
- use a higher simplify ratio
- clean non-manifold or broken triangles first
- keep `lod0` closer to original geometry

### KTX2 Pitfalls / KTX2 常见坑

| Issue | Cause | Fix |
| ----- | ----- | --- |
| Normal map rendering jitter | ETC1S block artifacts destroy normal precision | Force UASTC encoding for Normal textures |
| BaseColor color shift | Wrong color space label (Linear treated as sRGB or vice versa) | Mark BaseColor/Emissive as sRGB; Normal/ORM/AO as Linear |
| Larger file size than expected | UASTC without supercompression | Enable Zstd supercompression (`ktx2Options.supercompression: "zstd"`) |
| Black screen after loading | `KTX2Loader.detectSupport(renderer)` not called | Pass `renderer` when creating the loader |
| HDR environment map blown out | Color gamut truncation losing brightness | Use UASTC + Zstd encoding with HDR pipeline |
| Mipmap flickering | Poor implicit mipmap quality from encoder | Pre-generate mipmaps (`mipmapMode: "generate"`) and control filter mode |

## Escalate only when explicitly requested

仅当用户明确需要以下目标时，才切换到 Retopo + UV + Bake：
- editable low-poly assets / 可编辑低模
- clean topology / 干净拓扑
- game-engine editing / 游戏引擎深度编辑
- re-texturing workflows / 重新贴材质流程

要明确提醒：这是重制流程，不是简单压缩，成本显著更高。

## References

- `references/optimize-glb.mjs`: automation template for batch optimization, LOD generation, and manifest output；适合自动化处理与批量生成结果。
- `references/threejs-load-lod.js`: Three.js loading example for DRACO + LOD integration；适合前端接入与加载代码生成。
- `references/package-template.json`: minimal Node project template for running the optimization flow；适合初始化最小可运行工程。

## Response template

1. **Decision / 判断**：说明该任务应继续走 UV-safe optimization，还是升级到 Retopo + UV + Bake。
2. **Actions / 已执行项**：列出 cleanup、simplification、texture compression、LOD generation、manifest output、load validation。
3. **Results / 结果**：说明体积变化、几何压缩结果、LOD 输出和 Web loading status。
4. **Risks / 风险**：指出 blur、deformation、decode-path issues、loading bottlenecks 等问题。
5. **Next step / 下一步**：给出 tuning、splitting、lazy loading 或 engine integration 建议。
