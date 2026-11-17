# API Reference

Key API patterns for the libraries used in vibe web replication.

## Three.js (r169+)

### Core Setup

```javascript
import * as THREE from 'three';
import { GLTFLoader } from 'three/addons/loaders/GLTFLoader.js';
import { DRACOLoader } from 'three/addons/loaders/DRACOLoader.js';
import { EffectComposer } from 'three/addons/postprocessing/EffectComposer.js';
import { RenderPass } from 'three/addons/postprocessing/RenderPass.js';
import { UnrealBloomPass } from 'three/addons/postprocessing/UnrealBloomPass.js';

const scene = new THREE.Scene();
const camera = new THREE.PerspectiveCamera(50, w/h, 0.1, 1000);
camera.position.set(0, 0, 10);
const renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });
renderer.setSize(w, h);
renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
renderer.toneMapping = THREE.ACESFilmicToneMapping;
renderer.toneMappingExposure = 1.0;
document.getElementById('webgl').appendChild(renderer.domElement);
```

### Lights

```javascript
scene.add(new THREE.AmbientLight(0xffffff, 0.4));
const key = new THREE.DirectionalLight(0xffffff, 2.0);
key.position.set(5, 10, 7);
scene.add(key);
const rim = new THREE.PointLight(0x5e5ce6, 3, 50);
rim.position.set(-5, 2, -3);
scene.add(rim);
```

### GLB Loading (with Draco)

```javascript
const draco = new DRACOLoader();
draco.setDecoderPath('https://www.gstatic.com/draco/v1/decoders/');
const loader = new GLTFLoader();
loader.setDRACOLoader(draco);
loader.load('model.glb', (gltf) => {
  scene.add(gltf.scene);
  // play animations
  const mixer = new THREE.AnimationMixer(gltf.scene);
  gltf.animations.forEach(clip => mixer.clipAction(clip).play());
});
```

### Particles

```javascript
const count = 5000;
const positions = new Float32Array(count * 3);
for (let i = 0; i < count * 3; i++) positions[i] = (Math.random() - 0.5) * 50;
const geo = new THREE.BufferGeometry();
geo.setAttribute('position', new THREE.BufferAttribute(positions, 3));
const mat = new THREE.PointsMaterial({
  size: 0.05, color: 0x88ccff,
  transparent: true, opacity: 0.8,
  blending: THREE.AdditiveBlending
});
const points = new THREE.Points(geo, mat);
scene.add(points);
```

### Post-processing (Bloom)

```javascript
const composer = new EffectComposer(renderer);
composer.addPass(new RenderPass(scene, camera));
const bloom = new UnrealBloomPass(new THREE.Vector2(w, h), 1.5, 0.4, 0.85);
composer.addPass(bloom);
// In render loop: composer.render() instead of renderer.render()
```

---

## GSAP 3.12 + ScrollTrigger

### Register

```javascript
import gsap from 'gsap';
import { ScrollTrigger } from 'gsap/ScrollTrigger';
gsap.registerPlugin(ScrollTrigger);
```

### Pin + Scrub

```javascript
// Pin a section, animate 3D camera as you scroll through it
gsap.to(camera.position, {
  z: 2, y: 1,
  scrollTrigger: {
    trigger: '#hero',
    start: 'top top',
    end: '+=200%',    // super long section
    pin: true,
    scrub: 1,         // 1s lag for smoothness
    onUpdate: (self) => { /* self.progress 0→1 */ }
  }
});
```

### Timeline Chain

```javascript
const tl = gsap.timeline({
  scrollTrigger: {
    trigger: '#section2',
    start: 'top 80%',
    end: 'bottom 20%',
    scrub: 1
  }
});
tl.to('.title', { y: 0, opacity: 1, duration: 1 })
  .to('.subtitle', { opacity: 1, duration: 0.5 })
  .to('.card', { y: 0, opacity: 1, stagger: 0.1, duration: 0.8 });
```

### SplitText Reveal

```javascript
// Per-word reveal on headings
const heading = document.querySelector('h1');
// Manual split (no premium plugin needed):
const words = heading.textContent.split(' ');
heading.innerHTML = words.map(w => `<span class="word">${w}</span>`).join(' ');
gsap.from('.word', {
  yPercent: 100, opacity: 0,
  stagger: 0.05,
  scrollTrigger: { trigger: heading, start: 'top 85%' }
});
```

### Observer (Direction)

```javascript
ScrollTrigger.create({
  trigger: '#section',
  start: 'top center',
  onEnter: () => gsap.to('.element', { scale: 1.2 }),
  onLeaveBack: () => gsap.to('.element', { scale: 1 })
});
```

---

## Lenis (Smooth Scroll)

### Basic Setup

```javascript
import Lenis from 'lenis';
const lenis = new Lenis({
  duration: 1.2,
  easing: (t) => Math.min(1, 1.001 - Math.pow(2, -10 * t)),
  smoothWheel: true,
  // touch: { smoothTouch: false }  // disable on touch for native feel
});
function raf(time) {
  lenis.raf(time);
  requestAnimationFrame(raf);
}
requestAnimationFrame(raf);
```

### Lenis + ScrollTrigger Integration

```javascript
lenis.on('scroll', ScrollTrigger.update);
gsap.ticker.add((time) => lenis.raf(time * 1000));
gsap.ticker.lagSmoothing(0);
```

### ScrollTo

```javascript
document.querySelector('.cta').addEventListener('click', () => {
  lenis.scrollTo('#section2', { offset: 0 });
});
```

---

## Web Audio API

### Click-to-Unlock Pattern

```javascript
let audioCtx;
function unlockAudio() {
  if (audioCtx) return;
  audioCtx = new (window.AudioContext || window.webkitAudioContext)();
  // Resume if suspended
  if (audioCtx.state === 'suspended') audioCtx.resume();
}
document.addEventListener('click', unlockAudio, { once: true });

function playSound(url) {
  if (!audioCtx) return;
  fetch(url).then(r => r.arrayBuffer()).then(buf => {
    audioCtx.decodeAudioData(buf, (audioBuffer) => {
      const src = audioCtx.createBufferSource();
      const gain = audioCtx.createGain();
      gain.gain.value = 0.5;
      src.buffer = audioBuffer;
      src.connect(gain);
      gain.connect(audioCtx.destination);
      src.start();
    });
  });
}
```

---

## KTX2 Textures

```javascript
import { KTX2Loader } from 'three/addons/loaders/KTX2Loader.js';
const ktx2 = new KTX2Loader()
  .setTranscoderPath('https://cdn.jsdelivr.net/npm/three@0.169/examples/jsm/libs/basis/')
  .detectSupport(renderer);
const loader = new THREE.TextureLoader();
// For KTX2:
ktx2.load('texture.ktx2', (tex) => {
  tex.colorSpace = THREE.SRGBColorSpace;
  material.map = tex;
  material.needsUpdate = true;
});
```

---

## TagCloud.js

```javascript
import TagCloud from 'TagCloud';
const tags = TagCloud('.tag-container', ['AI', '3D', 'WebGL', 'GSAP', 'Vibe'], {
  radius: 250,
  maxSpeed: 'fast',
  initSpeed: 'fast',
  direction: 135,
  keep: true
});
```

---

## Vite Config

```javascript
// vite.config.js
import { defineConfig } from 'vite';
export default defineConfig({
  server: { port: 5173, open: true },
  build: {
    target: 'esnext',
    rollupOptions: {
      output: {
        manualChunks: {
          three: ['three'],
          gsap: ['gsap']
        }
      }
    }
  }
});
```
