import Lenis from 'lenis';
import gsap from 'gsap';
import { ScrollTrigger } from 'gsap/ScrollTrigger';
gsap.registerPlugin(ScrollTrigger);

// ── Initialize Lenis ────────────────────────────
const lenis = new Lenis({
  duration: 1.2,
  easing: (t) => Math.min(1, 1.001 - Math.pow(2, -10 * t)),
  smoothWheel: true,
  wheelMultiplier: 1.0,
  touchMultiplier: 2.0
});

// ── Sync Lenis → GSAP ScrollTrigger ─────────────
lenis.on('scroll', ScrollTrigger.update);
gsap.ticker.add((time) => {
  lenis.raf(time * 1000);
});
gsap.ticker.lagSmoothing(0);

// ── Click-to-scroll navigation ──────────────────
document.querySelectorAll('[data-scroll-to]').forEach(el => {
  el.addEventListener('click', (e) => {
    e.preventDefault();
    const target = el.getAttribute('data-scroll-to');
    lenis.scrollTo(target, { offset: 0, duration: 1.5 });
  });
});

// ── Audio unlock (optional) ─────────────────────
// Uncomment if using Web Audio
// let audioCtx;
// document.addEventListener('click', function unlock() {
//   audioCtx = new (window.AudioContext || window.webkitAudioContext)();
//   if (audioCtx.state === 'suspended') audioCtx.resume();
// }, { once: true });

export default lenis;
