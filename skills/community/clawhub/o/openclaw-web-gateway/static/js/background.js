(function () {
  const ui = window.JarvisUI;
  const canvas = document.getElementById("jarvis-bg");

  if (!canvas) return;

  const ctx = canvas.getContext("2d");

  let w = 0;
  let h = 0;
  let dpr = Math.max(1, Math.min(window.devicePixelRatio || 1, 2));
  let particles = [];
  let t = 0;

  function resizeCanvas() {
    w = window.innerWidth;
    h = window.innerHeight;
    dpr = Math.max(1, Math.min(window.devicePixelRatio || 1, 2));

    canvas.width = Math.floor(w * dpr);
    canvas.height = Math.floor(h * dpr);
    canvas.style.width = `${w}px`;
    canvas.style.height = `${h}px`;

    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    initParticles();
  }

  function initParticles() {
    const count = Math.min(160, Math.max(70, Math.floor((w * h) / 18000)));

    particles = Array.from({ length: count }, () => ({
      x: Math.random() * w,
      y: Math.random() * h,
      vx: (Math.random() - 0.5) * 0.22,
      vy: (Math.random() - 0.5) * 0.22,
      size: Math.random() * 1.8 + 0.4,
      alpha: Math.random() * 0.6 + 0.2,
    }));
  }

  function drawGrid() {
    ctx.save();
    ctx.strokeStyle = "rgba(70, 210, 255, 0.06)";
    ctx.lineWidth = 1;

    const spacing = 78;

    for (let x = ((t * 8) % spacing) - spacing; x < w + spacing; x += spacing) {
      ctx.beginPath();
      ctx.moveTo(x, 0);
      ctx.lineTo(x, h);
      ctx.stroke();
    }

    for (let y = ((t * 6) % spacing) - spacing; y < h + spacing; y += spacing) {
      ctx.beginPath();
      ctx.moveTo(0, y);
      ctx.lineTo(w, y);
      ctx.stroke();
    }

    ctx.restore();
  }

  function drawReactor() {
    const cx = w * 0.5;
    const cy = h * 0.56;
    const thinkingBoost = ui && ui.state.thinking ? 1 : 0;
    const pulse = 1 + Math.sin(t * 2.4) * (0.018 + thinkingBoost * 0.03);

    ctx.save();
    ctx.translate(cx, cy);
    ctx.scale(pulse, pulse);

    const halo = ctx.createRadialGradient(0, 0, 10, 0, 0, 280 + thinkingBoost * 90);
    halo.addColorStop(0, "rgba(110, 242, 255, 0.24)");
    halo.addColorStop(0.2, "rgba(57, 216, 255, 0.11)");
    halo.addColorStop(0.55, "rgba(30, 130, 255, 0.05)");
    halo.addColorStop(1, "rgba(0, 0, 0, 0)");

    ctx.fillStyle = halo;
    ctx.beginPath();
    ctx.arc(0, 0, 320 + thinkingBoost * 60, 0, Math.PI * 2);
    ctx.fill();

    for (let i = 0; i < 4; i++) {
      ctx.save();
      ctx.rotate(t * (0.12 + i * 0.03) * (i % 2 === 0 ? 1 : -1));
      ctx.strokeStyle = `rgba(95, 232, 255, ${0.12 - i * 0.02 + thinkingBoost * 0.04})`;
      ctx.lineWidth = i === 0 ? 2 : 1;
      ctx.beginPath();
      ctx.arc(0, 0, 70 + i * 28, 0, Math.PI * 1.55);
      ctx.stroke();
      ctx.restore();
    }

    ctx.strokeStyle = `rgba(130, 242, 255, ${0.22 + thinkingBoost * 0.2})`;
    ctx.lineWidth = 1;

    for (let i = 0; i < 18; i++) {
      const ang = (Math.PI * 2 / 18) * i + t * 0.15;
      const r1 = 34;
      const r2 = 120;

      ctx.beginPath();
      ctx.moveTo(Math.cos(ang) * r1, Math.sin(ang) * r1);
      ctx.lineTo(Math.cos(ang) * r2, Math.sin(ang) * r2);
      ctx.stroke();
    }

    const core = ctx.createRadialGradient(0, 0, 0, 0, 0, 54 + thinkingBoost * 10);
    core.addColorStop(0, "rgba(255,255,255,0.95)");
    core.addColorStop(0.14, "rgba(140,244,255,0.95)");
    core.addColorStop(0.4, "rgba(0,214,255,0.4)");
    core.addColorStop(1, "rgba(0,0,0,0)");

    ctx.fillStyle = core;
    ctx.beginPath();
    ctx.arc(0, 0, 58 + thinkingBoost * 12, 0, Math.PI * 2);
    ctx.fill();

    ctx.restore();
  }

  function drawSweep() {
    const thinking = ui && ui.state.thinking;
    const y = ((t * 120) % (h + 260)) - 130;
    const grad = ctx.createLinearGradient(0, y - 80, 0, y + 80);

    grad.addColorStop(0, "rgba(80, 220, 255, 0)");
    grad.addColorStop(0.5, `rgba(80, 220, 255, ${thinking ? 0.1 : 0.05})`);
    grad.addColorStop(1, "rgba(80, 220, 255, 0)");

    ctx.fillStyle = grad;
    ctx.fillRect(0, y - 80, w, 160);
  }

  function drawParticles() {
    const thinking = ui && ui.state.thinking;

    for (const p of particles) {
      p.x += p.vx * (thinking ? 1.35 : 1);
      p.y += p.vy * (thinking ? 1.35 : 1);

      if (p.x < -20) p.x = w + 20;
      if (p.x > w + 20) p.x = -20;
      if (p.y < -20) p.y = h + 20;
      if (p.y > h + 20) p.y = -20;

      ctx.beginPath();
      ctx.fillStyle = `rgba(120, 240, 255, ${p.alpha})`;
      ctx.arc(p.x, p.y, p.size + (thinking ? 0.15 : 0), 0, Math.PI * 2);
      ctx.fill();
    }

    ctx.save();
    ctx.strokeStyle = `rgba(100, 235, 255, ${thinking ? 0.12 : 0.06})`;
    ctx.lineWidth = 1;

    for (let i = 0; i < particles.length; i++) {
      for (let j = i + 1; j < particles.length; j++) {
        const a = particles[i];
        const b = particles[j];
        const dx = a.x - b.x;
        const dy = a.y - b.y;
        const dist = Math.hypot(dx, dy);
        const max = 95;

        if (dist < max) {
          ctx.globalAlpha = 1 - dist / max;
          ctx.beginPath();
          ctx.moveTo(a.x, a.y);
          ctx.lineTo(b.x, b.y);
          ctx.stroke();
        }
      }
    }

    ctx.restore();
    ctx.globalAlpha = 1;
  }

  function drawHudCorners() {
    ctx.save();
    ctx.strokeStyle = "rgba(112, 238, 255, 0.18)";
    ctx.lineWidth = 2;

    const pad = 18;
    const len = 40;
    const corners = [
      [pad, pad],
      [w - pad, pad],
      [pad, h - pad],
      [w - pad, h - pad],
    ];

    corners.forEach(([x, y], idx) => {
      ctx.beginPath();

      if (idx === 0) {
        ctx.moveTo(x + len, y);
        ctx.lineTo(x, y);
        ctx.lineTo(x, y + len);
      } else if (idx === 1) {
        ctx.moveTo(x - len, y);
        ctx.lineTo(x, y);
        ctx.lineTo(x, y + len);
      } else if (idx === 2) {
        ctx.moveTo(x + len, y);
        ctx.lineTo(x, y);
        ctx.lineTo(x, y - len);
      } else {
        ctx.moveTo(x - len, y);
        ctx.lineTo(x, y);
        ctx.lineTo(x, y - len);
      }

      ctx.stroke();
    });

    ctx.restore();
  }

  function animate() {
    const thinking = ui && ui.state.thinking;
    t += thinking ? 0.024 : 0.012;

    ctx.clearRect(0, 0, w, h);
    drawGrid();
    drawSweep();
    drawParticles();
    drawReactor();
    drawHudCorners();

    requestAnimationFrame(animate);
  }

  window.addEventListener("resize", resizeCanvas);
  resizeCanvas();
  animate();
})();
