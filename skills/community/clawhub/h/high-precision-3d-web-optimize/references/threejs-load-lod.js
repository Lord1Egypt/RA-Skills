import * as THREE from "three";
import { GLTFLoader } from "three/examples/jsm/loaders/GLTFLoader.js";
import { DRACOLoader } from "three/examples/jsm/loaders/DRACOLoader.js";
import { KTX2Loader } from "three/examples/jsm/loaders/KTX2Loader.js";

// 复用单一 KTX2Loader 实例，避免重复初始化
let sharedKTX2Loader = null;

/**
 * 获取或创建共享的 KTX2Loader 实例
 * 必须调用 detectSupport(renderer) 以选择最优 GPU 纹理格式
 */
function getKTX2Loader(renderer, ktx2TranscoderPath = "/basis/") {
  if (!sharedKTX2Loader) {
    sharedKTX2Loader = new KTX2Loader();
    sharedKTX2Loader.setTranscoderPath(ktx2TranscoderPath);
  }

  // 每次确保已绑定 renderer，detectSupport 内部会判断是否重复调用
  if (renderer) {
    sharedKTX2Loader.detectSupport(renderer);
  }

  return sharedKTX2Loader;
}

export function createGLTFLoader(options = {}) {
  const {
    dracoDecoderPath = "/draco/",
    // KTX2 相关配置
    textureCompression = "webp",
    renderer = null,
    ktx2TranscoderPath = "/basis/",
  } = options;

  const loader = new GLTFLoader();

  // Draco 解码器（始终启用）
  const dracoLoader = new DRACOLoader();
  dracoLoader.setDecoderPath(dracoDecoderPath);
  loader.setDRACOLoader(dracoLoader);

  // 当纹理格式为 KTX2 时，挂载 KTX2Loader
  if (textureCompression === "ktx2") {
    if (!renderer) {
      console.warn(
        "[loadLOD] textureCompression 为 ktx2 但未传入 renderer，" +
          "KTX2Loader.detectSupport() 无法执行，可能导致加载后黑屏。"
      );
    }
    const ktx2Loader = getKTX2Loader(renderer, ktx2TranscoderPath);
    loader.setKTX2Loader(ktx2Loader);
  }

  return loader;
}

export function loadGLB(loader, url) {
  return new Promise((resolve, reject) => {
    loader.load(url, (gltf) => resolve(gltf), undefined, (error) => reject(error));
  });
}

export async function loadTwinModelLOD(options) {
  const {
    basePath,
    name,
    // 从 manifest 读取纹理压缩格式，默认 webp 保持向后兼容
    textureCompression = "webp",
    renderer = null,
    ktx2TranscoderPath = "/basis/",
    loader = createGLTFLoader({
      textureCompression,
      renderer,
      ktx2TranscoderPath,
    }),
    distances = {
      lod0: 0,
      lod1: 35,
      lod2: 90,
    },
  } = options;

  const [lod0, lod1, lod2] = await Promise.all([
    loadGLB(loader, `${basePath}/${name}.lod0.glb`),
    loadGLB(loader, `${basePath}/${name}.lod1.glb`),
    loadGLB(loader, `${basePath}/${name}.lod2.glb`),
  ]);

  const lod = new THREE.LOD();

  lod.addLevel(lod0.scene, distances.lod0);
  lod.addLevel(lod1.scene, distances.lod1);
  lod.addLevel(lod2.scene, distances.lod2);

  lod.traverse((object) => {
    if (object.isMesh) {
      object.frustumCulled = true;
      object.castShadow = false;
      object.receiveShadow = false;
    }
  });

  return lod;
}
