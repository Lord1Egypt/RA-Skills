import * as THREE from 'three';
import { DRACOLoader } from 'three/addons/loaders/DRACOLoader.js';
import { GLTFLoader } from 'three/addons/loaders/GLTFLoader.js';
import { EffectComposer } from 'three/addons/postprocessing/EffectComposer.js';
import { RenderPass } from 'three/addons/postprocessing/RenderPass.js';
import { UnrealBloomPass } from 'three/addons/postprocessing/UnrealBloomPass.js';

// ── Scene ──────────────────────────────────────
const scene = new THREE.Scene();
scene.fog = new THREE.FogExp2(0x0a0a0f, 0.03);

const camera = new THREE.PerspectiveCamera(
  55, window.innerWidth / window.innerHeight, 0.1, 200
);
camera.position.set(0, 0, 12);

const renderer = new THREE.WebGLRenderer({
  antialias: true, alpha: true, powerPreference: 'high-performance'
});
renderer.setSize(window.innerWidth, window.innerHeight);
renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
renderer.toneMapping = THREE.ACESFilmicToneMapping;
renderer.toneMappingExposure = 1.2;
document.getElementById('webgl').appendChild(renderer.domElement);

// ── Lights ──────────────────────────────────────
scene.add(new THREE.AmbientLight(0xffffff, 0.3));
const keyLight = new THREE.DirectionalLight(0xffffff, 2.5);
keyLight.position.set(5, 8, 10);
scene.add(keyLight);
const accentLight = new THREE.PointLight(0x5e5ce6, 5, 60);
accentLight.position.set(-8, 3, -5);
scene.add(accentLight);
const rimLight = new THREE.PointLight(0x0a84ff, 3, 60);
rimLight.position.set(8, -2, 3);
scene.add(rimLight);

// ── Particle field ──────────────────────────────
const particleCount = 8000;
const positions = new Float32Array(particleCount * 3);
const colors = new Float32Array(particleCount * 3);
for (let i = 0; i < particleCount; i++) {
  positions[i*3]   = (Math.random() - 0.5) * 80;
  positions[i*3+1] = (Math.random() - 0.5) * 80;
  positions[i*3+2] = (Math.random() - 0.5) * 80;
  const c = Math.random();
  colors[i*3]   = c * 0.5 + 0.3;
  colors[i*3+1] = c * 0.4 + 0.4;
  colors[i*3+2] = c * 0.8 + 0.2;
}
const pGeo = new THREE.BufferGeometry();
pGeo.setAttribute('position', new THREE.BufferAttribute(positions, 3));
pGeo.setAttribute('color', new THREE.BufferAttribute(colors, 3));
const pMat = new THREE.PointsMaterial({
  size: 0.08, vertexColors: true,
  transparent: true, opacity: 0.7,
  blending: THREE.AdditiveBlending,
  depthWrite: false
});
const particles = new THREE.Points(pGeo, pMat);
scene.add(particles);

// ── Central object (procedural torus knot) ──────
const knotGeo = new THREE.TorusKnotGeometry(2, 0.6, 200, 32);
const knotMat = new THREE.MeshStandardMaterial({
  color: 0x5e5ce6, metalness: 0.8, roughness: 0.2,
  emissive: 0x1a1a4e, emissiveIntensity: 0.5
});
const knot = new THREE.Mesh(knotGeo, knotMat);
scene.add(knot);

// ── Post-processing (Bloom) ──────────────────────
const composer = new EffectComposer(renderer);
composer.addPass(new RenderPass(scene, camera));
const bloomPass = new UnrealBloomPass(
  new THREE.Vector2(window.innerWidth, window.innerHeight),
  1.2,   // strength
  0.5,   // radius
  0.85   // threshold
);
composer.addPass(bloomPass);

// ── GLB Loader (optional) ───────────────────────
const draco = new DRACOLoader();
draco.setDecoderPath('https://www.gstatic.com/draco/v1/decoders/');
const gltfLoader = new GLTFLoader();
gltfLoader.setDRACOLoader(draco);
// Uncomment to load a model:
// gltfLoader.load('/model.glb', (gltf) => {
//   scene.add(gltf.scene);
// });

// ── Animation state (updated by main.js scroll) ─
export const state = {
  scrollProgress: 0,
  mouseX: 0,
  mouseY: 0
};

// ── Render loop ─────────────────────────────────
const clock = new THREE.Clock();
export function animate() {
  const elapsed = clock.getElapsedTime();
  const sp = state.scrollProgress;

  // Rotate knot
  knot.rotation.x = elapsed * 0.3 + sp * 2;
  knot.rotation.y = elapsed * 0.2 + sp * 3;

  // Move camera on scroll (push in, then pan)
  camera.position.z = 12 - sp * 8;        // 12 → 4
  camera.position.y = sp * 3;             // 0 → 3
  camera.position.x = Math.sin(sp * Math.PI) * 2;
  camera.lookAt(0, sp * 2, 0);

  // Slight camera parallax from mouse
  camera.position.x += state.mouseX * 0.5;
  camera.position.y += state.mouseY * 0.3;

  // Rotate particles slowly
  particles.rotation.y = elapsed * 0.05;
  particles.rotation.x = sp * 0.5;

  composer.render();
  requestAnimationFrame(animate);
}

// ── Resize ──────────────────────────────────────
window.addEventListener('resize', () => {
  camera.aspect = window.innerWidth / window.innerHeight;
  camera.updateProjectionMatrix();
  renderer.setSize(window.innerWidth, window.innerHeight);
  composer.setSize(window.innerWidth, window.innerHeight);
});

// ── Mouse tracking ──────────────────────────────
window.addEventListener('mousemove', (e) => {
  state.mouseX = (e.clientX / window.innerWidth - 0.5);
  state.mouseY = -(e.clientY / window.innerHeight - 0.5);
});

// Start
animate();
