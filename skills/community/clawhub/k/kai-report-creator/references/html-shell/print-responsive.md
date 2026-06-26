# Print and Responsive Rules

        @page { size: A4; margin: 1.5cm; }
        @media print {
          * { -webkit-print-color-adjust: exact !important; print-color-adjust: exact !important; }
          html, body {
            background: var(--print-bg-color, var(--report-bg, var(--bg, #ffffff))) !important;
            color: var(--report-text, var(--text, #111111)) !important;
          }
          .toc-toggle, .toc-sidebar, .edit-hotzone, .edit-toggle, .export-btn, .export-menu { display: none !important; }
          h2 { break-after: avoid; }
          .kpi-grid, .kpi-card, .callout, .timeline, .timeline-item,
          .table-wrapper, [data-component="chart"], .diagram-wrapper { break-inside: avoid; }
          .chart-container { height: 200px !important; }
          canvas { max-height: 200px !important; width: 100% !important; }
          img { max-height: 260px !important; width: auto !important; object-fit: contain; }
          .fade-in-up { opacity: 1 !important; transform: translateY(0) !important; }
          .kpi-grid .kpi-card, .timeline .timeline-item { opacity: 1 !important; transform: none !important; }
        }

        /* Responsive rule: never hide critical functionality (export, edit toggle, KPI values, charts) on mobile.
           Only decorative/progressive-enhancement elements (animations, TOC overlay) may be suppressed. */
        body.no-toc .toc-sidebar, body.no-toc .toc-toggle { display: none; }
        body.no-toc .main-with-toc { margin-left: 0; }
