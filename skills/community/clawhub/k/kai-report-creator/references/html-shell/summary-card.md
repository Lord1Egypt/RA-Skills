# Summary Card

        /* Summary card button — bottom-aligned with h1 */
        .title-row { display: flex; align-items: flex-end; gap: 1rem; }
        .title-row h1 { flex: 1; }
        .card-mode-btn {
          flex-shrink: 0; margin-bottom: .6rem;
          background: var(--surface); border: 1px solid var(--border); border-radius: 4px;
          padding: .28rem .65rem; font-size: .76rem; font-weight: 600;
          color: var(--text-muted); cursor: pointer; transition: all .15s;
          font-family: var(--font-sans, system-ui); white-space: nowrap;
        }
        .card-mode-btn:hover { background: var(--primary-light); color: var(--primary); border-color: var(--primary); }

        /* Summary card overlay */
        .sc-overlay {
          display: none; position: fixed; inset: 0; z-index: 500;
          background: rgba(0,0,0,.52); backdrop-filter: blur(6px);
          align-items: center; justify-content: center; padding: 2rem;
        }
        body.card-mode .sc-overlay { display: flex; }
        body.card-mode { overflow: hidden; height: 100vh; }
        html:has(body.card-mode) { overflow: hidden; height: 100vh; }
        body.card-mode .main-with-toc,
        body.card-mode .toc-toggle,
        body.card-mode .toc-sidebar { visibility: hidden; }
        body.card-mode .sc-overlay { visibility: visible; }

        /* Card — editorial two-column, high density */
        .sc-card {
          position: relative; display: flex; width: min(900px, 92vw);
          background: #fff; border: 1px solid rgba(0,0,0,.12);
          border-radius: 8px; overflow: hidden;
          box-shadow: 0 24px 72px rgba(0,0,0,.3);
        }
        /* Left panel */
        .sc-left {
          flex: 0 0 46%; display: flex; flex-direction: column;
          padding: 1.8rem 2rem 1.6rem;
          background: var(--primary); color: #fff;
        }
        .sc-label {
          font-size: .55rem; font-weight: 700; letter-spacing: .18em; text-transform: uppercase;
          opacity: .5; margin-bottom: .55rem; display: flex; align-items: center; gap: .45rem;
        }
        .sc-label::before { content: ''; display: inline-block; width: 20px; height: 1px; background: currentColor; }
        /* poster title should dominate the card */
        .sc-title-main {
          font-size: clamp(3.45rem, 6.9vw, 5.25rem);
          font-weight: 900;
          line-height: .92;
          letter-spacing: -.05em;
          margin-bottom: .35rem;
          word-break: break-word;
        }
        .sc-title-sub {
          font-size: 1.08rem;
          line-height: 1.5;
          color: rgba(255,255,255,.88);
          margin-bottom: .9rem;
          max-width: 82%;
        }
        .sc-note {
          margin-top: auto;
          padding-top: 1.4rem;
          width: 72%;
          font-size: .84rem;
          line-height: 1.68;
          opacity: .9;
        }
        /* Right panel */
        .sc-right {
          flex: 1; display: flex; flex-direction: column;
          padding: 1.8rem 1.8rem 1.8rem;
          border-left: 1px solid var(--border);
        }
        /* KPI rows — compact 2-col, no card boxes */
        .sc-kpi-rows { display: grid; grid-template-columns: 1fr 1fr; gap: 0 .6rem; margin-bottom: .5rem; }
        .sc-kpi-row { padding: .32rem 0; border-bottom: 1px solid var(--border); }
        .sc-kpi-row-l { font-size: .56rem; color: var(--text-muted); text-transform: uppercase; letter-spacing: .06em; }
        .sc-kpi-row-v { font-size: 1.15rem; font-weight: 800; color: var(--primary); line-height: 1.15; }
        .sc-kpi-row-t { font-size: .6rem; color: var(--success, #057A55); font-weight: 600; }
        /* Section summaries — divider rows */
        .sc-summaries { flex: 1; display: flex; flex-direction: column; }
        .sc-sum-item { padding: .35rem 0; border-bottom: 1px solid var(--border); }
        .sc-sum-item:last-child { border-bottom: none; }
        .sc-sum-name { font-size: .56rem; font-weight: 700; color: var(--primary); text-transform: uppercase; letter-spacing: .08em; }
        .sc-sum-text { font-size: .74rem; color: var(--text); line-height: 1.45; margin-top: .06rem; opacity: .72; }
        /* Close button */
        .sc-close {
          position: absolute; top: .8rem; right: .8rem; z-index: 1;
          background: rgba(255,255,255,.15); border: 1px solid rgba(255,255,255,.25); border-radius: 3px;
          width: 24px; height: 24px; cursor: pointer; color: #fff;
          display: flex; align-items: center; justify-content: center; font-size: .75rem;
          transition: background .15s;
        }
        .sc-close:hover { background: rgba(255,255,255,.28); }
        @media (max-width: 900px) {
          .action-grid { grid-template-columns: 1fr; }
          .sc-card { flex-direction: column; width: min(92vw, 640px); }
          .sc-right { border-left: none; border-top: 1px solid var(--border); }
        }
        @media print { .sc-overlay, .card-mode-btn { display: none !important; } }

          <!-- Report title and meta -->
          <!-- lang:en card button label: "⊞ Summary" | lang:zh: "⊞ 摘要卡" -->
          <div class="title-row">
            <h1>[title]</h1>
            <button class="card-mode-btn" id="card-mode-btn" title="[Summary card|摘要卡片]">[⊞ Summary|⊞ 摘要卡]</button>
          </div>
          [if abstract: <p class="report-subtitle">[abstract]</p>]
          [if author or date: <p class="report-meta">[author] · [date]</p>]

          <!-- Summary card overlay (always present) — left+right panels injected by buildCard() -->
          <div class="sc-overlay" id="sc-overlay">
            <div class="sc-card" id="sc-card">
              <button class="sc-close" id="sc-close" aria-label="Close">✕</button>
              <!-- .sc-left and .sc-right injected by JS -->

      <script>
        // Summary card — editorial two-column layout, built from #report-summary JSON + DOM data-summary
        (function() {
          const btn      = document.getElementById('card-mode-btn');
          const overlay  = document.getElementById('sc-overlay');
          const closeBtn = document.getElementById('sc-close');
          if (!btn || !overlay) return;

          function splitPosterTitle(d) {
            const explicitTitle = (d.poster_title || '').trim();
            const explicitSubtitle = (d.poster_subtitle || '').trim();
            const raw = (d.title || '').trim();
            return { main: explicitTitle || raw, sub: explicitTitle ? explicitSubtitle : '' };
          }

          function summaryCardLabel() {
            const lang = (document.documentElement.lang || '').toLowerCase();
            return lang.startsWith('zh') ? '报告摘要' : 'Report Summary';
          }

          function posterNoteText(d) {
            const explicit = (d.poster_note || '').trim();
            if (explicit) return explicit;
            const raw = (d.abstract || '').trim();
            if (!raw) return '';
            const sentence = raw.match(/^(.{0,72}?[。！？!?]|.{0,120})/)?.[1]?.trim() || raw;
            return sentence.length > 72 ? sentence.slice(0, 72).trim() + '…' : sentence;
          }

          function buildCard() {
            try {
              const d = JSON.parse(document.getElementById('report-summary').textContent);
              const poster = splitPosterTitle(d);
              const note = posterNoteText(d);

              // Left panel: poster title hierarchy + one short closing sentence near the bottom.
              const leftHtml = `
                <div class="sc-left">
                  <div class="sc-label">${summaryCardLabel()}</div>
                  <div class="sc-title-main">${poster.main || ''}</div>
                  ${poster.sub ? `<div class="sc-title-sub">${poster.sub}</div>` : ''}
                  ${note ? `<div class="sc-note">${note}</div>` : ''}
                </div>`;

              // Right panel: compact KPI rows + section summaries only. Keep the card poster-like.
              const kpiRowsHtml = (d.kpis || []).slice(0, 6).map(k => `
                <div class="sc-kpi-row">
                  <div class="sc-kpi-row-l">${k.label || ''}</div>
                  <div class="sc-kpi-row-v">${k.value || ''}${k.trend ? ` <span class="sc-kpi-row-t">${k.trend}</span>` : ''}</div>
                </div>`).join('');
              const sectionSummaries = Array.from(
                document.querySelectorAll('section[data-section]')
              ).map(s => ({ name: s.dataset.section || '', text: s.dataset.summary || '' }))
               .filter(s => s.name)
               .slice(0, 3);
              const summariesHtml = sectionSummaries.map(s => `
                <div class="sc-sum-item">
                  <div class="sc-sum-name">${s.name}</div>
                  ${s.text ? `<div class="sc-sum-text">${s.text}</div>` : ''}
                </div>`).join('');
              const rightHtml = `
                <div class="sc-right">
                  ${kpiRowsHtml ? `<div class="sc-kpi-rows">${kpiRowsHtml}</div>` : ''}
                  ${summariesHtml ? `<div class="sc-summaries" style="margin-top:.5rem">${summariesHtml}</div>` : ''}
                </div>`;

              const card = document.getElementById('sc-card');
              card.insertAdjacentHTML('beforeend', leftHtml + rightHtml);
            } catch(e) {
              const card = document.getElementById('sc-card');
              card.insertAdjacentHTML('beforeend', '<div style="padding:2rem;color:#666">Summary unavailable.</div>');
            }
          }

          let built = false;
          function openCard() {
            if (!built) { buildCard(); built = true; }
            document.body.classList.add('card-mode');
            overlay.setAttribute('aria-hidden', 'false');
          }
          function closeCard() {
            document.body.classList.remove('card-mode');
            overlay.setAttribute('aria-hidden', 'true');
          }

          btn.addEventListener('click', openCard);
          closeBtn && closeBtn.addEventListener('click', closeCard);
          overlay.addEventListener('click', e => { if (e.target === overlay) closeCard(); });
          document.addEventListener('keydown', e => {
            if (e.key === 'Escape' && document.body.classList.contains('card-mode')) closeCard();
          });
        })();
      </script>
