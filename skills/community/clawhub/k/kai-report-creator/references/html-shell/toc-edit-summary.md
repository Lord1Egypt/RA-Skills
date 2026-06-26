# TOC, Edit Mode, and Motion

        /* Edit mode */
        .edit-hotzone { position: fixed; bottom: 0; left: 0; width: 80px; height: 80px; z-index: 10000; cursor: pointer; }
        .edit-toggle { position: fixed; bottom: 16px; left: 16px; background: var(--primary); color: #fff; border: none; border-radius: 6px; padding: .45rem .9rem; font-size: .82rem; cursor: pointer; font-weight: 600; opacity: 0; pointer-events: none; transition: opacity .25s ease, background .2s ease; z-index: 10001; box-shadow: 0 2px 8px rgba(0,0,0,.25); letter-spacing: .02em; }
        .edit-toggle.show { opacity: 1; pointer-events: auto; }
        .edit-toggle.active { opacity: 1; pointer-events: auto; background: var(--success); }
        body.edit-mode [contenteditable] { outline: 1px dashed var(--border); border-radius: 2px; cursor: text; }
        body.edit-mode [contenteditable]:hover { outline-color: var(--primary); }
        body.edit-mode [contenteditable]:focus { outline: 2px solid var(--primary); }

        /* Floating TOC overlay — default collapsed on all screen sizes */
        .toc-sidebar {
          position: fixed; top: 0; left: 0; width: 240px; height: 100vh;
          overflow-y: auto; padding: 3rem 1rem 1.5rem; background: var(--surface);
          border-right: 1px solid var(--border); font-size: .83rem; z-index: 100;
          transform: translateX(-100%); transition: transform .28s ease;
        }
        .toc-sidebar.open {
          transform: translateX(0); box-shadow: 4px 0 24px rgba(0,0,0,.18);
        }
        .toc-sidebar h4 {
          font-size: .72rem; text-transform: uppercase; letter-spacing: .08em;
          color: var(--text-muted); margin: 0 0 .75rem; font-weight: 600;
        }
        .toc-sidebar a {
          display: block; color: var(--text-muted); text-decoration: none;
          padding: .28rem .5rem; border-radius: 4px; margin-bottom: 1px; transition: all .18s;
          white-space: nowrap; overflow: hidden; text-overflow: ellipsis;
        }
        .toc-sidebar a:hover, .toc-sidebar a.active { color: var(--primary); background: var(--primary-light); }
        .toc-sidebar a.toc-h3 { padding-left: 1.1rem; font-size: .78rem; opacity: .85; }
        .main-with-toc { margin-left: 0; }
        .toc-toggle {
          position: fixed; top: .75rem; left: .75rem; z-index: 200;
          background: var(--primary); color: #fff; border: none; border-radius: 6px;
          padding: .45rem .7rem; cursor: pointer; font-size: 1rem; line-height: 1;
          box-shadow: 0 2px 8px rgba(0,0,0,.2);
        }
        .toc-toggle.locked { box-shadow: 0 0 0 2px #fff, 0 2px 8px rgba(0,0,0,.2); }
        @media (max-width: 768px) {
          .report-wrapper { padding: 1.5rem 1rem; }
        }
        /* Responsive rule: never hide critical functionality (export, edit toggle, KPI values, charts) on mobile.
           Only decorative/progressive-enhancement elements (animations, TOC overlay) may be suppressed. */
        body.no-toc .toc-sidebar, body.no-toc .toc-toggle { display: none; }
        body.no-toc .main-with-toc { margin-left: 0; }

      <!-- Edit mode (always present) -->
      <div class="edit-hotzone" id="edit-hotzone"></div>
      <button class="edit-toggle" id="edit-toggle" title="Edit mode (E)">✏ Edit</button>

      <!-- Floating TOC (omit entirely if toc:false) -->
      <!-- TOC label localization: lang:en → aria-label="Contents" / "Table of Contents" / <h4>Contents</h4> -->
      <!--                         lang:zh → aria-label="目录" / "报告目录" / <h4>目录</h4> -->
      <button class="toc-toggle" id="toc-toggle-btn" aria-label="[Contents|目录]" aria-expanded="false">☰</button>
      <nav class="toc-sidebar" id="toc-sidebar" aria-label="[Table of Contents|报告目录]">
        <h4>[Contents|目录]</h4>
        <!-- Generate one <a> per ## heading and one per ### heading in the report -->
        <!-- Example (lang:en): <a href="#section-core-metrics" data-section="Core Metrics">Core Metrics</a> -->
        <!-- For ### heading: add class="toc-h3" -->
        [TOC links generated from all ## and ### headings in the IR]
      </nav>

      <script>
        // Scroll-triggered animations
        if (!document.body.classList.contains('no-animations')) {
          // Generic fade-in-up
          const fadeObserver = new IntersectionObserver(
            entries => entries.forEach(e => {
              if (e.isIntersecting) { e.target.classList.add('visible'); fadeObserver.unobserve(e.target); }
            }),
            { threshold: 0.08 }
          );
          document.querySelectorAll('.fade-in-up').forEach(el => fadeObserver.observe(el));

          // Stagger helper: observe parent, animate children one by one
          function staggerGroup(parentSel, childSel, delay) {
            document.querySelectorAll(parentSel).forEach(parent => {
              new IntersectionObserver((entries, obs) => {
                if (!entries[0].isIntersecting) return;
                obs.disconnect();
                parent.classList.add('stagger-ready');
                parent.querySelectorAll(childSel).forEach((el, i) =>
                  setTimeout(() => el.classList.add('visible'), i * delay)
                );
              }, { threshold: 0.1 }).observe(parent);
            });
          }
          staggerGroup('.kpi-grid', '.kpi-card', 100);   // KPI cards: spring bounce stagger
          staggerGroup('.timeline', '.timeline-item', 130); // Timeline items: slide-in stagger

          // KPI counter animation (CountUp)
          const kpiObserver = new IntersectionObserver(entries => {
            entries.forEach(e => {
              if (!e.isIntersecting) return;
              const el = e.target;
              const target = parseFloat(el.dataset.targetValue);
              if (isNaN(target)) return;
              const prefix = el.dataset.prefix || '';
              const suffix = el.dataset.suffix || '';
              const isFloat = String(target).includes('.');
              const decimals = isFloat ? String(target).split('.')[1].length : 0;
              let startTime = null;
              const duration = 1200;
              const animate = ts => {
                if (!startTime) startTime = ts;
                const progress = Math.min((ts - startTime) / duration, 1);
                const ease = 1 - Math.pow(1 - progress, 3);
                const current = isFloat
                  ? (ease * target).toFixed(decimals)
                  : Math.floor(ease * target).toLocaleString();
                el.textContent = prefix + current + suffix;
                if (progress < 1) requestAnimationFrame(animate);
                else el.textContent = prefix + (isFloat ? target.toFixed(decimals) : target.toLocaleString()) + suffix;
              };
              requestAnimationFrame(animate);
              kpiObserver.unobserve(el);
            });
          }, { threshold: 0.3 });
          document.querySelectorAll('.kpi-value[data-target-value]').forEach(el => kpiObserver.observe(el));
        }

        // TOC: hover to open, click to lock, no backdrop
        const tocBtn = document.getElementById('toc-toggle-btn');
        const tocSidebar = document.getElementById('toc-sidebar');
        if (tocBtn && tocSidebar) {
          let locked = false, closeTimer;
          function openToc() {
            clearTimeout(closeTimer);
            tocSidebar.classList.add('open');
            tocBtn.setAttribute('aria-expanded', 'true');
          }
          function scheduleClose() {
            closeTimer = setTimeout(() => {
              if (!locked) {
                tocSidebar.classList.remove('open');
                tocBtn.setAttribute('aria-expanded', 'false');
              }
            }, 150);
          }
          tocBtn.addEventListener('mouseenter', openToc);
          tocSidebar.addEventListener('mouseenter', openToc);
          tocBtn.addEventListener('mouseleave', scheduleClose);
          tocSidebar.addEventListener('mouseleave', scheduleClose);
          tocBtn.addEventListener('click', () => {
            locked = !locked;
            tocBtn.classList.toggle('locked', locked);
            if (locked) openToc(); else scheduleClose();
          });
          document.querySelectorAll('.toc-sidebar a').forEach(a => a.addEventListener('click', () => {
            if (!locked) scheduleClose();
          }));
        }

        // TOC active state tracking
        const tocLinks = document.querySelectorAll('.toc-sidebar a[data-section]');
        if (tocLinks.length) {
          const sectionObserver = new IntersectionObserver(entries => {
            entries.forEach(e => {
              const id = e.target.dataset.section;
              const link = document.querySelector(`.toc-sidebar a[data-section="${CSS.escape(id)}"]`);
              if (link) link.classList.toggle('active', e.isIntersecting);
            });
          }, { rootMargin: '-10% 0px -60% 0px' });
          document.querySelectorAll('section[data-section]').forEach(s => sectionObserver.observe(s));
        }
      </script>

      <script>
        // Edit mode: hover bottom-left hotzone to reveal button, click to toggle
        (function() {
          const hotzone = document.getElementById('edit-hotzone');
          const toggle  = document.getElementById('edit-toggle');
          if (!hotzone || !toggle) return;
          let active = false, hideTimer;
          function showBtn() { clearTimeout(hideTimer); toggle.classList.add('show'); }
          function schedHide() { hideTimer = setTimeout(() => { if (!active) toggle.classList.remove('show'); }, 400); }
          hotzone.addEventListener('mouseenter', showBtn);
          hotzone.addEventListener('mouseleave', schedHide);
          toggle.addEventListener('mouseenter', showBtn);
          toggle.addEventListener('mouseleave', schedHide);
          function enterEdit() {
            active = true; toggle.classList.add('active', 'show'); toggle.textContent = '✓ Done';
            document.body.classList.add('edit-mode');
            document.querySelectorAll('h1,h2,h3,p,li,td,th,figcaption').forEach(el => el.setAttribute('contenteditable', 'true'));
          }
          function exitEdit() {
            active = false; toggle.classList.remove('active'); toggle.textContent = '✏ Edit';
            document.body.classList.remove('edit-mode');
            document.querySelectorAll('[contenteditable]').forEach(el => el.removeAttribute('contenteditable'));
            schedHide();
          }
          hotzone.addEventListener('click', () => active ? exitEdit() : enterEdit());
          toggle.addEventListener('click', () => active ? exitEdit() : enterEdit());
          document.addEventListener('keydown', e => {
            if ((e.key === 'e' || e.key === 'E') && !document.activeElement.getAttribute('contenteditable')) {
              active ? exitEdit() : enterEdit();
            }
            if ((e.ctrlKey || e.metaKey) && e.key === 's') {
              e.preventDefault();
              const html = '<!DOCTYPE html>\n' + document.documentElement.outerHTML;
              const a = Object.assign(document.createElement('a'), {
                href: URL.createObjectURL(new Blob([html], {type: 'text/html'})),
                download: location.pathname.split('/').pop() || 'report.html'
              });
              a.click(); URL.revokeObjectURL(a.href);
            }
          });
        })();
      </script>
