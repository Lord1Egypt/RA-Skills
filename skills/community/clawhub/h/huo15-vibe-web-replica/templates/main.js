// ── Main entry: wires everything together ───────
// This is the file loaded by index.html

// 1. Three.js scene (3D rendering + post-processing)
import './three-scene.js';

// 2. GSAP scroll animations (ScrollTrigger + timeline chains)
import './gsap-scroll.js';

// 3. Lenis smooth scroll (synced with GSAP ticker)
import './lenis-setup.js';

// 4. Optional: TagCloud, Audio, etc.
// import TagCloud from 'tagcloud';
// const tc = TagCloud('.tag-container', ['AI','3D','WebGL'], { radius: 250 });
