import gsap from 'gsap';
import { ScrollTrigger } from 'gsap/ScrollTrigger';
gsap.registerPlugin(ScrollTrigger);

// ── Hero title: word-by-word reveal ─────────────
function splitWords(el) {
  const words = el.textContent.split(' ');
  el.innerHTML = words.map(w =>
    `<span class="word"><span class="word-inner">${w}</span></span>`
  ).join(' ');
}
splitWords(document.getElementById('hero-title'));

gsap.to('#hero-title .word-inner', {
  y: 0,
  duration: 1,
  stagger: 0.08,
  ease: 'power3.out',
  scrollTrigger: {
    trigger: '#hero',
    start: 'top top',
    toggleActions: 'play none none reverse'
  }
});

// ── Hero: pin + scrub ───────────────────────────
gsap.to('.hero-inner', {
  opacity: 0,
  scale: 0.8,
  y: -100,
  scrollTrigger: {
    trigger: '#hero',
    start: 'top top',
    end: 'bottom bottom',
    scrub: 1,
    pin: false
  }
});

// ── Features section ────────────────────────────
// Section title slides in
gsap.from('#features-title', {
  x: -100,
  opacity: 0,
  duration: 1,
  scrollTrigger: {
    trigger: '#features',
    start: 'top 80%'
  }
});

// Feature cards stagger in
gsap.from('.feature-card', {
  y: 80,
  opacity: 0,
  duration: 0.8,
  stagger: 0.15,
  scrollTrigger: {
    trigger: '#features',
    start: 'top 70%'
  }
});

// Parallax: cards drift slightly as you scroll
gsap.to('.feature-card', {
  yPercent: -20,
  scrollTrigger: {
    trigger: '#features',
    start: 'top top',
    end: 'bottom top',
    scrub: 1
  }
});

// ── CTA section: scale in ───────────────────────
gsap.from('#cta h2', {
  scale: 0.5,
  opacity: 0,
  duration: 1,
  scrollTrigger: {
    trigger: '#cta',
    start: 'top 70%'
  }
});

gsap.from('.cta-button', {
  y: 50,
  opacity: 0,
  duration: 0.8,
  delay: 0.3,
  scrollTrigger: {
    trigger: '#cta',
    start: 'top 70%'
  }
});

// ── 3D scene sync: update scroll progress ───────
// This connects GSAP scroll to the Three.js camera
import { state } from './three-scene.js';
ScrollTrigger.create({
  trigger: 'body',
  start: 'top top',
  end: 'bottom bottom',
  onUpdate: (self) => {
    state.scrollProgress = self.progress;
  }
});
