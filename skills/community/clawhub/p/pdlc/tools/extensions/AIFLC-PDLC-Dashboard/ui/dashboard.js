/**
 * AIT-VSC Dashboard — Shared Rendering Logic
 * Works in both VS Code webview and standalone browser mode.
 * Expects `var D` to be defined (data object) before this script loads.
 */

// === MODE DETECTION ===
var isVSCode = (typeof acquireVsCodeApi !== 'undefined');
var vscode = isVSCode ? acquireVsCodeApi() : null;

var selectedProject = null;
var statusColors = { complete: '#4caf50', active: '#ff9800', pending: '#bdbdbd', blocked: '#f44336' };
var statusEmojis = { complete: '\u2705', active: '\uD83D\uDD04', pending: '\u2B1C', blocked: '\uD83D\uDEAB' };
var packageNames = {
  'AI-ILC': 'Idea Life Cycle', 'AI-PILC': 'Project Initiation',
  'AI-POLC': 'Product Ownership', 'AI-UXD': 'UX Design',
  'AI-ADLC': 'Architecture Design', 'AI-DWG': 'Workspace Generator',
  'AI-PPM': 'Portfolio Management', 'AI-FLO': 'Flow Orchestrator',
  'AI-GCE': 'Governance & Compliance', 'AI-TGE': 'Test Engine'
};
var kanbanColColors = {
  captured: '#888', shaped: '#569cd6', evaluated: '#ff9800',
  scoped: '#9c27b0', approved: '#4caf50', routed: '#2196f3',
  parked: '#795548', rejected: '#f44336'
};

// === THEME ===
function toggleTheme() {
  var html = document.documentElement;
  var next = html.getAttribute('data-theme') === 'dark' ? 'light' : 'dark';
  html.setAttribute('data-theme', next);
  localStorage.setItem('ait-theme', next);
}
function loadTheme() {
  var saved = localStorage.getItem('ait-theme');
  if (saved) document.documentElement.setAttribute('data-theme', saved);
}

// === LEFT PANEL TOGGLE ===
function toggleLeftPanel() {
  var panel = document.getElementById('panel-left');
  var btn = document.getElementById('panel-toggle');
  var isCollapsed = panel.classList.toggle('collapsed');
  btn.classList.toggle('collapsed', isCollapsed);
  var isPortrait = window.innerWidth <= 1024;
  if (isPortrait) {
    btn.innerHTML = isCollapsed ? '&#x25BC;' : '&#x25B2;';
  } else {
    btn.innerHTML = isCollapsed ? '&gt;' : '&lt;';
  }
}
// Fix arrow on resize
window.addEventListener('resize', function() {
  var btn = document.getElementById('panel-toggle');
  var panel = document.getElementById('panel-left');
  if (!btn || !panel) return;
  var isCollapsed = panel.classList.contains('collapsed');
  var isPortrait = window.innerWidth <= 1024;
  if (isPortrait) { btn.innerHTML = isCollapsed ? '&#x25BC;' : '&#x25B2;'; }
  else { btn.innerHTML = isCollapsed ? '&gt;' : '&lt;'; }
});

// === ARTIFACT OPEN ===
function openArtifact(path, evt) {
  if (evt) evt.stopPropagation();
  if (vscode) { vscode.postMessage({ type: 'openFile', path: path }); return; }
  // Browser mode
  if (!path || path === '' || path.startsWith('http')) return;
  console.log('[Dashboard] openArtifact:', path);
  // Skip folder paths (ending with /)
  var isFolder = path.charAt(path.length - 1) === '/';

  var modal = document.getElementById('file-preview-modal');
  if (!modal) {
    modal = document.createElement('div');
    modal.id = 'file-preview-modal';
    modal.className = 'file-preview-modal';
    modal.innerHTML = '<div class="file-preview-overlay" onclick="closeFilePreview()"></div><div class="file-preview-box"><div class="file-preview-header"><span class="file-preview-path"></span><button onclick="closeFilePreview()">\u2715</button></div><div class="file-preview-body"></div></div>';
    document.body.appendChild(modal);
  }
  modal.querySelector('.file-preview-path').textContent = path;
  var body = modal.querySelector('.file-preview-body');

  if (isFolder) {
    body.classList.remove('md-rendered');
    body.textContent = 'Folder: ' + path + '\n\nThis is a directory containing multiple files.\nExpand the topic in the document list to see individual files.';
    modal.classList.add('visible');
    return;
  }

  var ext = path.split('.').pop().toLowerCase();
  var isText = (ext === 'md' || ext === 'txt' || ext === 'json' || ext === 'yaml' || ext === 'yml');

  if (isText && window.location.protocol !== 'file:') {
    // HTTP mode: fetch and render content
    body.textContent = 'Loading...';
    body.classList.remove('md-rendered');
    modal.classList.add('visible');
    fetch(path).then(function(r) {
      if (!r.ok) throw new Error(r.status);
      return r.text();
    }).then(function(text) {
      if (ext === 'md') {
        body.innerHTML = renderMarkdown(text);
        body.classList.add('md-rendered');
      } else {
        body.textContent = text;
        body.classList.remove('md-rendered');
      }
    }).catch(function() {
      body.classList.remove('md-rendered');
      body.textContent = 'File: ' + path + '\n\nCould not load file content.';
    });
  } else if (isText && window.location.protocol === 'file:') {
    // file:// mode: use XMLHttpRequest synchronous (works in some browsers) or show path
    body.classList.remove('md-rendered');
    var loaded = false;
    try {
      var xhr = new XMLHttpRequest();
      xhr.open('GET', path, false);
      xhr.send();
      if (xhr.status === 0 || xhr.status === 200) {
        var text = xhr.responseText;
        if (text && text.length > 0) {
          if (ext === 'md') {
            body.innerHTML = renderMarkdown(text);
            body.classList.add('md-rendered');
          } else {
            body.textContent = text;
          }
          loaded = true;
        }
      }
    } catch(e) { /* expected in strict CORS browsers */ }
    if (!loaded) {
      body.textContent = 'File: ' + path + '\n\nBrowser blocks file:// access (CORS).\n\nTo preview files, serve this folder:\n  npx serve .\nThen open http://localhost:3000\n\nOr use the VS Code extension for direct file access.';
    }
    modal.classList.add('visible');
  } else {
    body.classList.remove('md-rendered');
    body.textContent = 'File: ' + path + '\n\nBinary or non-text file.\nIn VS Code extension mode, this opens directly in the editor.';
    modal.classList.add('visible');
  }
}

// Simple markdown renderer (headings, bold, italic, lists, code blocks, links)
function renderMarkdown(md) {
  var html = md
    .replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;')
    .replace(/^### (.+)$/gm, '<h4>$1</h4>')
    .replace(/^## (.+)$/gm, '<h3>$1</h3>')
    .replace(/^# (.+)$/gm, '<h2>$1</h2>')
    .replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>')
    .replace(/\*(.+?)\*/g, '<em>$1</em>')
    .replace(/`([^`]+)`/g, '<code>$1</code>')
    .replace(/^\- (.+)$/gm, '<li>$1</li>')
    .replace(/^\d+\. (.+)$/gm, '<li>$1</li>')
    .replace(/\[([^\]]+)\]\(([^)]+)\)/g, '<a href="$2" target="_blank">$1</a>')
    .replace(/^---$/gm, '<hr>')
    .replace(/\n\n/g, '</p><p>')
    .replace(/\n/g, '<br>');
  return '<p>' + html + '</p>';
}

function closeFilePreview() {
  var modal = document.getElementById('file-preview-modal');
  if (modal) modal.classList.remove('visible');
}
function toggleDocSub(id, event) {
  event.stopPropagation();
  var el = document.getElementById(id);
  if (!el) return;
  el.classList.toggle('expanded');
  var btn = event.target;
  btn.textContent = el.classList.contains('expanded') ? '\u25BC' : '\u25B6';
}

// === TABS ===
function initTabs(containerId) {
  var container = document.getElementById(containerId);
  var tabs = container.querySelectorAll('.tab');
  tabs.forEach(function(tab) {
    tab.addEventListener('click', function() {
      tabs.forEach(function(t) { t.classList.remove('active'); });
      tab.classList.add('active');
      var target = tab.getAttribute('data-tab');
      var parent = container.parentElement;
      parent.querySelectorAll('.tab-content').forEach(function(c) { c.classList.remove('active'); });
      var el = document.getElementById('tc-' + target);
      if (el) el.classList.add('active');
      if (target === 'chain' && selectedProject) renderChain(selectedProject);
    });
  });
}

// === SELECT PROJECT ===
function selectProject(id) {
  selectedProject = D.projects.find(function(p) { return p.id === id; });
  if (!selectedProject) return;
  document.getElementById('right-header').textContent = selectedProject.name;
  document.getElementById('overall-badge').textContent = D.health.overallProgress + '%';
  // Show/hide domain tabs based on data availability
  var poTab = document.querySelector('[data-tab="po"]');
  var poExtTab = document.querySelector('[data-tab="po-ext"]');
  var archTab = document.querySelector('[data-tab="architect"]');
  var uxTab = document.querySelector('[data-tab="ux"]');
  if (poTab) poTab.style.display = '';
  if (poExtTab) poExtTab.style.display = '';
  if (archTab) archTab.style.display = '';
  if (uxTab) uxTab.style.display = '';
  saveGroupStates();
  renderPortfolio();
  restoreGroupStates();
  renderPM();
  renderPO();
  renderArch();
  renderUX();
  renderMgmt();
  renderStatsRight();
}

// === PORTFOLIO TAB ===
function renderPortfolio() {
  var el = document.getElementById('tc-portfolio');
  var dispatched = D.projects.filter(function(p) { return p.status !== 'pending'; }).length;
  var pending = D.projects.filter(function(p) { return p.status === 'pending'; }).length;
  var html = '<div class="health-grid">';
  html += '<div class="health-item"><div class="health-value">' + D.projects.length + '</div><div class="health-label">Total Projects</div></div>';
  html += '<div class="health-item"><div class="health-value">' + dispatched + '</div><div class="health-label">Dispatched</div></div>';
  html += '<div class="health-item"><div class="health-value">' + pending + '</div><div class="health-label">Pending</div></div>';
  html += '<div class="health-item"><div class="health-value">' + D.health.totalBlockers + '</div><div class="health-label">Blocked</div></div>';
  html += '<div class="health-item"><div class="health-value">' + D.health.overallProgress + '%</div><div class="health-label">Progress</div></div>';
  html += '<div class="health-item"><div class="health-value">' + D.health.stalledProjects + '</div><div class="health-label">Stalled</div></div>';
  html += '</div>';
  var groups = [
    { key: 'dispatched', label: 'Dispatched', filter: function(p) { return p.status === 'active' || p.status === 'blocked'; }, open: true },
    { key: 'pending', label: 'Pending', filter: function(p) { return p.status === 'pending'; }, open: true },
    { key: 'complete', label: 'Complete', filter: function(p) { return p.status === 'complete'; }, open: false }
  ];
  groups.forEach(function(g) {
    var items = D.projects.filter(g.filter);
    html += '<div class="group-section' + (g.open ? '' : ' collapsed') + '" id="group-' + g.key + '">';
    html += '<div class="group-header" onclick="toggleGroup(\'' + g.key + '\')"><span class="group-arrow">\u25BC</span> ' + g.label + ' (' + items.length + ')</div>';
    html += '<div class="group-body">';
    items.forEach(function(p) {
      var sel = (selectedProject && selectedProject.id === p.id) ? ' selected' : '';
      var fc = p.status === 'complete' ? '#4caf50' : '#ff9800';
      html += '<div class="project-row' + sel + '" onclick="selectProject(\'' + p.id + '\')"><span class="status-dot" style="background:' + statusColors[p.status] + '"></span><span class="name">' + p.name + '</span><span class="progress-mini"><span class="progress-mini-fill" style="width:' + p.progress + '%;background:' + fc + '"></span></span><span class="pct">' + p.progress + '%</span></div>';
    });
    html += '</div></div>';
  });
  el.innerHTML = html;
}
function toggleGroup(key) { document.getElementById('group-' + key).classList.toggle('collapsed'); }

// Track portfolio group states
var portfolioGroupStates = {};
function saveGroupStates() {
  ['dispatched','pending','complete'].forEach(function(k) {
    var el = document.getElementById('group-' + k);
    if (el) portfolioGroupStates[k] = el.classList.contains('collapsed');
  });
}
function restoreGroupStates() {
  ['dispatched','pending','complete'].forEach(function(k) {
    var el = document.getElementById('group-' + k);
    if (el && portfolioGroupStates[k] !== undefined) {
      if (portfolioGroupStates[k]) el.classList.add('collapsed');
      else el.classList.remove('collapsed');
    }
  });
}

// === IDEAS TAB ===
function renderIdeas() {
  var el = document.getElementById('tc-ideas');
  if (!D.ideas || D.ideas.length === 0) { el.innerHTML = '<div class="empty-state">No ideas tracked</div>'; return; }
  var stages = ['captured','shaped','evaluated','scoped','approved','routed','parked','rejected'];
  var html = '';
  stages.forEach(function(stage) {
    var items = D.ideas.filter(function(i) { return i.stage === stage; });
    if (items.length === 0) return;
    var colColor = kanbanColColors[stage] || '#888';
    html += '<div class="idea-group" id="idea-grp-' + stage + '">';
    html += '<div class="idea-group-hdr" onclick="toggleIdeaGroup(\'' + stage + '\')" style="border-left-color:' + colColor + ';"><span class="idea-grp-arrow">\u25BC</span><span class="idea-grp-label">' + stage + '</span><span class="idea-grp-count">' + items.length + '</span></div>';
    html += '<div class="idea-group-body">';
    items.forEach(function(idea, idx) {
      var scoreHtml = '';
      if (idea.score !== null) { var sc = idea.score >= 30 ? '#4caf50' : (idea.score >= 20 ? '#ff9800' : '#f44336'); scoreHtml = '<span class="idea-card-score" style="color:' + sc + '">' + idea.score + '/35</span>'; }
      var ideaId = 'idea-' + stage + '-' + idx;
      html += '<div class="idea-card" id="' + ideaId + '" style="border-left-color:' + colColor + ';">';
      html += '<div class="idea-card-hdr" onclick="toggleIdeaCard(\'' + ideaId + '\',event)"><span class="idea-card-title">' + idea.name + '</span>' + scoreHtml + '</div>';
      // Expandable detail inline
      html += '<div class="idea-card-body">';
      html += '<div class="idea-card-brief">' + idea.brief + '</div>';
      html += '<div class="idea-card-meta"><span>Domain: ' + idea.domain + '</span></div>';
      if (idea.route) { var rl = {'new-project':'\uD83D\uDE80 New Project','feature-backlog':'\uD83D\uDCCB Feature Backlog','change-request':'\uD83D\uDD04 Change Request'}; html += '<div class="idea-card-route">' + (rl[idea.route]||idea.route) + (idea.routeTarget ? ' \u2192 ' + idea.routeTarget : '') + '</div>'; }
      if (idea.reason) html += '<div class="idea-card-reason">' + idea.reason + '</div>';
      var files = idea.files || idea.artifacts || [];
      if (files.length > 0) {
        html += '<div class="idea-card-files"><strong>Files:</strong>';
        files.forEach(function(f) {
          var icon = f.status === 'produced' ? '\u2705' : (f.status === 'in-progress' ? '\uD83D\uDD04' : '\u23F3');
          var link = f.path ? '<a href="#" onclick="openArtifact(\'' + f.path.replace(/'/g, "\\'") + '\',event);return false;">' + f.name + '</a>' : f.name;
          html += '<div class="idea-card-file">' + icon + ' ' + link + '</div>';
        });
        html += '</div>';
      }
      html += '</div></div>';
    });
    html += '</div></div>';
  });
  el.innerHTML = html;
}
function toggleIdeaGroup(stage) {
  document.getElementById('idea-grp-' + stage).classList.toggle('collapsed');
}
function toggleIdeaCard(id, evt) {
  if (evt) evt.stopPropagation();
  var el = document.getElementById(id);
  if (el) el.classList.toggle('expanded');
}

// === STATS LEFT ===
function renderStatsLeft() {
  var el = document.getElementById('tc-stats-left');
  var counts = { Active: 0, Complete: 0, Pending: 0, Blocked: 0 };
  D.projects.forEach(function(p) { var k = p.status.charAt(0).toUpperCase()+p.status.slice(1); if (counts[k] !== undefined) counts[k]++; });
  var colors1 = { Active: '#ff9800', Complete: '#4caf50', Pending: '#bdbdbd', Blocked: '#f44336' };

  var totalArtifacts = 0, doneArtifacts = 0, totalBlockers = 0;
  D.projects.forEach(function(p) { p.packages.forEach(function(pkg) { totalArtifacts += pkg.progress.total; doneArtifacts += pkg.progress.done; pkg.blockers.forEach(function() { totalBlockers++; }); }); });

  var html = '';

  // === Portfolio Health Ring ===
  html += '<div class="pmx-hero" style="margin-bottom:14px;">';
  html += '<div class="pmx-ring-wrap"><svg class="pmx-ring" viewBox="0 0 100 100"><circle cx="50" cy="50" r="42" fill="none" stroke="var(--bg-hover)" stroke-width="8"/><circle cx="50" cy="50" r="42" fill="none" stroke="#4caf50" stroke-width="8" stroke-dasharray="' + (D.health.overallProgress * 2.64) + ' 264" stroke-linecap="round" transform="rotate(-90 50 50)"/><text x="50" y="46" text-anchor="middle" font-size="18" font-weight="700" fill="var(--text-heading)">' + D.health.overallProgress + '%</text><text x="50" y="60" text-anchor="middle" font-size="7" fill="var(--text-secondary)">PORTFOLIO</text></svg></div>';
  html += '<div class="pmx-hero-stats"><div class="pmx-stat"><span class="pmx-stat-val" style="color:#4caf50;">' + counts.Complete + '</span><span class="pmx-stat-lbl">Complete</span></div><div class="pmx-stat"><span class="pmx-stat-val" style="color:#ff9800;">' + counts.Active + '</span><span class="pmx-stat-lbl">Active</span></div><div class="pmx-stat"><span class="pmx-stat-val" style="color:#f44336;">' + (counts.Blocked || 0) + '</span><span class="pmx-stat-lbl">Blocked</span></div><div class="pmx-stat"><span class="pmx-stat-val">' + D.projects.length + '</span><span class="pmx-stat-lbl">Total</span></div></div>';
  html += '</div>';

  // === Project Progress Cards (mini ring per project) ===
  html += '<div class="stats-section-title">Projects</div>';
  html += '<div class="stats-project-grid">';
  var sorted = D.projects.slice().sort(function(a,b) { return b.progress - a.progress; });
  sorted.forEach(function(p) {
    var c = p.status==='complete'?'#4caf50':(p.status==='blocked'?'#f44336':'#ff9800');
    var shortName = p.name.length > 16 ? p.name.substring(0,16)+'\u2026' : p.name;
    html += '<div class="stats-proj-card"><svg viewBox="0 0 44 44" class="stats-mini-ring"><circle cx="22" cy="22" r="18" fill="none" stroke="var(--bg-hover)" stroke-width="4"/><circle cx="22" cy="22" r="18" fill="none" stroke="'+c+'" stroke-width="4" stroke-dasharray="'+(p.progress*1.13)+' 113" stroke-linecap="round" transform="rotate(-90 22 22)"/><text x="22" y="24" text-anchor="middle" font-size="9" font-weight="700" fill="var(--text-heading)">'+p.progress+'</text></svg><span class="stats-proj-name">'+shortName+'</span></div>';
  });
  html += '</div>';

  // === Ideas Pipeline Visual ===
  if (D.ideas && D.ideas.length > 0) {
    var stages = ['captured','shaped','evaluated','scoped','approved','routed','parked','rejected'];
    var sc = {}; stages.forEach(function(s) { sc[s] = D.ideas.filter(function(i) { return i.stage === s; }).length; });
    var stageColors = {captured:'#888',shaped:'#569cd6',evaluated:'#ff9800',scoped:'#9c27b0',approved:'#4caf50',routed:'#2196f3',parked:'#795548',rejected:'#f44336'};
    var total = D.ideas.length;

    html += '<div class="stats-section-title">Ideas (' + total + ')</div>';
    html += '<div class="stats-ideas-flow">';
    stages.forEach(function(s) {
      if (sc[s] === 0) return;
      var pct = Math.round(sc[s]/total*100);
      html += '<div class="stats-idea-seg" style="flex:' + sc[s] + ';background:' + stageColors[s] + ';" title="' + s + ': ' + sc[s] + '"></div>';
    });
    html += '</div><div class="stats-ideas-legend">';
    stages.forEach(function(s) { if (sc[s] > 0) html += '<span class="stats-idea-lbl"><span class="stats-idea-dot" style="background:' + stageColors[s] + ';"></span>' + s + ' ' + sc[s] + '</span>'; });
    html += '</div>';
  }

  // === Package Chain Health ===
  html += '<div class="stats-section-title">Package Chain</div>';
  var pkgHealth = {};
  D.projects.forEach(function(p) { p.packages.forEach(function(pkg) { if (!pkgHealth[pkg.code]) pkgHealth[pkg.code] = {complete:0,active:0,pending:0,blocked:0,total:0}; pkgHealth[pkg.code][pkg.status]++; pkgHealth[pkg.code].total++; }); });
  html += '<div class="stats-chain-grid">';
  ['AI-ILC','AI-PILC','AI-POLC','AI-UXD','AI-ADLC','AI-DWG','AI-GCE','AI-TGE'].forEach(function(code) {
    var h = pkgHealth[code]; if (!h) return;
    var pct = h.total>0?Math.round(h.complete/h.total*100):0;
    var c = pct>=75?'#4caf50':(pct>=25?'#ff9800':'#616161');
    html += '<div class="stats-chain-cell" style="border-color:'+c+';"><span class="stats-chain-code">'+code.replace('AI-','')+'</span><span class="stats-chain-pct" style="color:'+c+';">'+pct+'%</span></div>';
  });
  html += '</div>';

  el.innerHTML = html;
}

// === PM TAB ===
function renderPM() {
  if (!selectedProject) return;
  var el = document.getElementById('tc-pm');
  var p = selectedProject;
  var html = '';

  // === PM Visual Overview (from PM-ext) ===
  var totalPkgs = p.packages.length;
  var completePkgs = p.packages.filter(function(pk){return pk.status==='complete'}).length;
  var activePkgs = p.packages.filter(function(pk){return pk.status==='active'}).length;
  var blockedPkgs = p.packages.filter(function(pk){return pk.status==='blocked'}).length;
  var pendingPkgs = totalPkgs - completePkgs - activePkgs - blockedPkgs;
  var chainOrder = ['AI-ILC','AI-PILC','AI-POLC','AI-UXD','AI-ADLC','AI-DWG','AI-GCE','AI-TGE'];

  // Progress Ring + Stats
  html += '<div class="pmx-hero">';
  html += '<div class="pmx-ring-wrap"><svg class="pmx-ring" viewBox="0 0 100 100"><circle cx="50" cy="50" r="42" fill="none" stroke="var(--bg-hover)" stroke-width="8"/><circle cx="50" cy="50" r="42" fill="none" stroke="#4caf50" stroke-width="8" stroke-dasharray="' + (p.progress * 2.64) + ' 264" stroke-linecap="round" transform="rotate(-90 50 50)"/><text x="50" y="46" text-anchor="middle" font-size="18" font-weight="700" fill="var(--text-heading)">' + p.progress + '%</text><text x="50" y="60" text-anchor="middle" font-size="7" fill="var(--text-secondary)">COMPLETE</text></svg></div>';
  html += '<div class="pmx-hero-stats"><div class="pmx-stat"><span class="pmx-stat-val" style="color:#4caf50;">' + completePkgs + '</span><span class="pmx-stat-lbl">Done</span></div><div class="pmx-stat"><span class="pmx-stat-val" style="color:#ff9800;">' + activePkgs + '</span><span class="pmx-stat-lbl">Active</span></div><div class="pmx-stat"><span class="pmx-stat-val" style="color:#f44336;">' + blockedPkgs + '</span><span class="pmx-stat-lbl">Blocked</span></div><div class="pmx-stat"><span class="pmx-stat-val" style="color:#bdbdbd;">' + pendingPkgs + '</span><span class="pmx-stat-lbl">Pending</span></div></div>';
  html += '</div>';

  // Package Lifecycle Swimlane
  html += '<div class="pmx-timeline-title">Package Lifecycle</div>';
  html += '<div class="pmx-timeline">';
  chainOrder.forEach(function(code) {
    var pkg = p.packages.find(function(pk){return pk.code === code});
    if (!pkg) return;
    var pName = (packageNames[code] || code).split(' ')[0];
    var barColor = pkg.status==='complete'?'#4caf50':(pkg.status==='active'?'#ff9800':(pkg.status==='blocked'?'#f44336':'#616161'));
    var emoji = statusEmojis[pkg.status];
    html += '<div class="pmx-lane"><div class="pmx-lane-label"><span class="pmx-lane-code">' + code.replace('AI-','') + '</span><span class="pmx-lane-name">' + pName + '</span></div><div class="pmx-lane-track"><div class="pmx-lane-bar" style="width:' + pkg.progress.pct + '%;background:' + barColor + ';"><span class="pmx-lane-pct">' + (pkg.progress.pct > 15 ? pkg.progress.pct + '%' : '') + '</span></div></div><span class="pmx-lane-emoji">' + emoji + '</span></div>';
  });
  html += '</div>';

  // Blockers
  var allBlockersTop = [];
  p.packages.forEach(function(pkg) { pkg.blockers.forEach(function(b) { allBlockersTop.push({ source: pkg.code, text: b }); }); });
  if (allBlockersTop.length > 0) {
    html += '<div class="pmx-blockers"><div class="pmx-blockers-title">\uD83D\uDEA8 Blockers (' + allBlockersTop.length + ')</div>';
    allBlockersTop.forEach(function(b) { html += '<div class="pmx-blocker"><span class="pmx-blocker-src">' + b.source + '</span><span class="pmx-blocker-text">' + b.text + '</span></div>'; });
    html += '</div>';
  }

  // Artifact Heatmap
  html += '<div class="pmx-heatmap-title">Artifact Heatmap</div>';
  html += '<div class="pmx-heatmap">';
  chainOrder.forEach(function(code) {
    var pkg = p.packages.find(function(pk){return pk.code === code});
    if (!pkg || !pkg.artifacts) return;
    html += '<div class="pmx-heatmap-row"><span class="pmx-heatmap-label">' + code.replace('AI-','') + '</span><div class="pmx-heatmap-cells">';
    pkg.artifacts.forEach(function(a) {
      var color = a.status==='produced'?'#4caf50':(a.status==='in-progress'?'#ff9800':'#333');
      html += '<div class="pmx-cell" style="background:' + color + ';" title="' + a.name + ' (' + a.status + ')"></div>';
    });
    html += '</div></div>';
  });
  html += '</div>';

  // DRACIL Summary
  var mgmt = p.mgmt || {};
  var mgmtD = p.mgmtDetail || {};
  html += '<div class="pmx-timeline-title">Management Framework (DRACIL)</div>';
  html += '<div class="pmx-dracil">';
  [{key:'decisions',icon:'\uD83D\uDCCB',label:'Decisions',color:'#569cd6'},{key:'risks',icon:'\u26A0\uFE0F',label:'Risks',color:'#f44336'},{key:'actions',icon:'\u2705',label:'Actions',color:'#4caf50'},{key:'changes',icon:'\uD83D\uDD04',label:'Changes',color:'#ff9800'},{key:'issues',icon:'\uD83D\uDC1B',label:'Issues',color:'#e91e63'},{key:'lessons',icon:'\uD83D\uDCA1',label:'Lessons',color:'#9c27b0'}].forEach(function(d) {
    var count = mgmt[d.key] || 0;
    var items = mgmtD[d.key] || [];
    var openCount = items.filter(function(i){var s=(i.status||'').toLowerCase(); return s==='open'||s==='in progress'||s==='pending'||s==='proposed'||s==='investigating'||s==='mitigating';}).length;
    html += '<div class="pmx-dracil-item" style="border-left-color:' + d.color + ';"><div class="pmx-dracil-icon">' + d.icon + '</div><div class="pmx-dracil-body"><div class="pmx-dracil-label">' + d.label + '</div><div class="pmx-dracil-counts"><span class="pmx-dracil-total">' + count + '</span>' + (openCount > 0 ? '<span class="pmx-dracil-open">' + openCount + ' open</span>' : '<span class="pmx-dracil-clear">all clear</span>') + '</div></div></div>';
  });
  html += '</div>';

  // Critical Path
  html += '<div class="pmx-timeline-title">Critical Path</div>';
  html += '<div class="pmx-critical-path">';
  var criticalPkg = null;
  for (var ci = 0; ci < chainOrder.length; ci++) { var cpkg = p.packages.find(function(pk){return pk.code === chainOrder[ci]}); if (cpkg && (cpkg.status === 'active' || cpkg.status === 'blocked')) { criticalPkg = cpkg; break; } }
  if (criticalPkg) {
    var cpColor = criticalPkg.status === 'blocked' ? '#f44336' : '#ff9800';
    var cpName = packageNames[criticalPkg.code] || criticalPkg.code;
    var remaining = criticalPkg.progress.total - criticalPkg.progress.done;
    html += '<div class="pmx-cp-card" style="border-left-color:' + cpColor + ';"><div class="pmx-cp-head"><span class="pmx-cp-code" style="color:' + cpColor + ';">' + criticalPkg.code + '</span><span class="pmx-cp-name">' + cpName + '</span></div>';
    html += '<div class="pmx-cp-detail">Phase ' + criticalPkg.phase.c + '/' + criticalPkg.phase.t + ' \u00B7 ' + criticalPkg.stage.name + '</div>';
    html += '<div class="pmx-cp-detail">' + remaining + ' artifacts remaining \u00B7 ' + criticalPkg.progress.pct + '% complete</div>';
    if (criticalPkg.blockers.length > 0) { html += '<div class="pmx-cp-blocker">\uD83D\uDEA8 ' + criticalPkg.blockers[0] + '</div>'; }
    html += '<div class="pmx-cp-bar"><div class="pmx-cp-bar-fill" style="width:' + criticalPkg.progress.pct + '%;background:' + cpColor + ';"></div></div></div>';
  } else { html += '<div style="font-size:11px;color:#4caf50;padding:8px;">\u2705 No active bottleneck.</div>'; }
  html += '</div>';

  // Chain Readiness
  html += '<div class="pmx-timeline-title">Chain Readiness</div>';
  html += '<div class="pmx-chain-ready">';
  for (var ri = 0; ri < chainOrder.length; ri++) {
    var rpkg = p.packages.find(function(pk){return pk.code === chainOrder[ri]});
    if (!rpkg) continue;
    var rColor = rpkg.status==='complete'?'#4caf50':(rpkg.status==='active'?'#ff9800':(rpkg.status==='blocked'?'#f44336':'#616161'));
    var rReady = rpkg.status === 'complete'; var nextPkg = (ri < chainOrder.length - 1) ? p.packages.find(function(pk){return pk.code === chainOrder[ri+1]}) : null;
    var handoffReady = rReady && nextPkg && nextPkg.status !== 'complete';
    html += '<div class="pmx-chain-node" style="border-color:' + rColor + ';' + (handoffReady?'box-shadow:0 0 6px '+rColor+'44;':'') + '"><span class="pmx-chain-code" style="color:' + rColor + ';">' + chainOrder[ri].replace('AI-','') + '</span><span class="pmx-chain-status">' + (rpkg.status==='complete'?'\u2705':(rpkg.status==='active'?'\u26A1':(rpkg.status==='blocked'?'\uD83D\uDEAB':'\u23F3'))) + '</span></div>';
    if (ri < chainOrder.length - 1) { var arrowColor = rReady ? '#4caf50' : 'var(--border)'; html += '<div class="pmx-chain-arrow" style="color:' + arrowColor + ';">\u2192</div>'; }
  }
  html += '</div>';

  // === Separator before existing PM content ===
  html += '<div style="border-top:1px solid var(--border);margin:16px 0;"></div>';

  // === Original PM Content (Package Cards) ===
  html += '<h3 style="color:var(--text-heading);font-size:14px;margin-bottom:10px;">Package Details</h3>';
  p.packages.forEach(function(pkg, idx) {
    var pName = packageNames[pkg.code] || pkg.code;
    var emoji = statusEmojis[pkg.status];
    var phaseLabel = pkg.status === 'complete' ? 'Complete' : 'Phase ' + pkg.phase.c + '/' + pkg.phase.t + ' \u00B7 ' + pkg.phase.name;
    var fillClass = pkg.status === 'complete' ? 'complete' : 'active';
    // Build artifact/document list for expanded detail
    var artHtml = '';
    var arts = pkg.artifacts || [];
    if (arts.length > 0) {
      var producedCount = arts.filter(function(a){return a.status==='produced'}).length;
      var inProgressCount = arts.filter(function(a){return a.status==='in-progress'}).length;
      var pendingCount = arts.filter(function(a){return a.status==='pending'}).length;
      artHtml = '<div style="margin-top:10px;"><strong style="font-size:12px;">Documents (' + arts.length + '):</strong>';
      artHtml += '<div class="doc-filters" data-pkg="' + idx + '"><span class="doc-filter active" onclick="filterDocs(' + idx + ',\'all\',event)">All ' + arts.length + '</span><span class="doc-filter" onclick="filterDocs(' + idx + ',\'produced\',event)">\uD83D\uDFE2 ' + producedCount + '</span><span class="doc-filter" onclick="filterDocs(' + idx + ',\'in-progress\',event)">\uD83D\uDD04 ' + inProgressCount + '</span><span class="doc-filter" onclick="filterDocs(' + idx + ',\'pending\',event)">\u26AA ' + pendingCount + '</span></div>';
      artHtml += '<div class="pkg-doc-list" id="doc-list-' + idx + '">';
      arts.forEach(function(a, ai) {
        var dotCls = a.status === 'produced' ? 'dot-produced' : (a.status === 'in-progress' ? 'dot-active' : 'dot-pending');
        var hasFiles = a.files && a.files.length > 0;
        var link = '<a href="#" onclick="openArtifact(\'' + (a.path||'').replace(/'/g, "\\'") + '\',event);return false;">' + a.name + '</a>';
        if (hasFiles) {
          // Multi-file topic: parent row is just topic label + count, detail lives on sub-files
          var expandBtn = '<span class="doc-expand-btn" onclick="toggleDocSub(\'docsub-' + idx + '-' + ai + '\',event)">\u25B6</span>';
          artHtml += '<div class="doc-row doc-row-topic" data-docstatus="' + a.status + '">' + expandBtn + '<span class="doc-dot ' + dotCls + '"></span><span class="doc-name">' + a.name + '</span><span class="doc-meta"><span>' + a.files.length + ' files</span></span></div>';
          artHtml += '<div class="doc-subfiles" id="docsub-' + idx + '-' + ai + '">';
          a.files.forEach(function(sf) {
            var sfDot = sf.status === 'produced' ? 'dot-produced' : (sf.status === 'in-progress' ? 'dot-active' : 'dot-pending');
            var sfLink = sf.path ? '<a href="#" onclick="openArtifact(\'' + sf.path.replace(/'/g, "\\'") + '\',event);return false;">' + sf.name + '</a>' : sf.name;
            var sfMeta = '';
            if (sf.updatedAt) sfMeta += '<span>' + sf.updatedAt + '</span>';
            if (sf.owner) sfMeta += '<span>' + sf.owner + '</span>';
            artHtml += '<div class="doc-subfile"><span class="doc-dot ' + sfDot + '"></span><span class="doc-sf-name">' + sfLink + '</span><span class="doc-meta">' + sfMeta + '</span></div>';
          });
          artHtml += '</div>';
        } else {
          // Single file: show all detail inline
          var meta = '';
          if (a.updatedAt) meta += '<span>' + a.updatedAt + '</span>';
          if (a.owner) meta += '<span>' + a.owner + '</span>';
          artHtml += '<div class="doc-row" data-docstatus="' + a.status + '"><span class="doc-dot ' + dotCls + '"></span><span class="doc-name">' + link + '</span><span class="doc-meta">' + meta + '</span></div>';
        }
      });
      artHtml += '</div></div>';
    } else if (pkg.status === 'pending') {
      artHtml = '<div style="margin-top:10px;font-size:12px;color:var(--text-secondary);font-style:italic;">No documents yet \u2014 package not started</div>';
    }
    html += '<div class="card" id="pkg-card-' + idx + '" onclick="toggleCard(\'pkg-card-' + idx + '\',event)"><div class="card-hdr"><span>' + emoji + '</span><span class="card-title">' + pName + ' (' + pkg.code + ')</span></div><div class="card-phase">' + phaseLabel + '</div><div class="progress-bar"><div class="progress-fill ' + fillClass + '" style="width:' + pkg.progress.pct + '%"></div></div><div class="card-meta"><span>' + pkg.progress.done + '/' + pkg.progress.total + ' artifacts</span><span>' + pkg.progress.pct + '%</span></div><div class="card-detail"><p><strong>Stage:</strong> ' + pkg.stage.name + '</p>' + (pkg.blockers.length > 0 ? '<p style="color:#f44336;margin-top:4px;"><strong>Blockers:</strong> ' + pkg.blockers.join('; ') + '</p>' : '') + artHtml + '</div></div>';
  });
  var allBlockers = [];
  p.packages.forEach(function(pkg) { pkg.blockers.forEach(function(b) { allBlockers.push({ source: pkg.code, text: b }); }); });
  if (allBlockers.length > 0) {
    html += '<h3 style="color:var(--text-heading);font-size:14px;margin:16px 0 10px;">Blockers (' + allBlockers.length + ')</h3>';
    allBlockers.forEach(function(b, idx) { html += '<div class="blocker-item" id="blocker-' + idx + '" onclick="toggleBlocker(\'blocker-' + idx + '\')"><div class="source">' + b.source + '</div><div class="text">' + b.text + '</div><div class="detail">Escalation recommended if unresolved within 48 hours.</div></div>'; });
  }
  el.innerHTML = html;
}
function toggleCard(id, evt) { 
  var e = evt || window.event;
  if (e && e.target) {
    var t = e.target;
    // Don't toggle if click was inside the document list, filters, or on interactive elements
    if (t.tagName === 'A' || t.tagName === 'BUTTON' || t.closest('.pkg-doc-list') || t.closest('.doc-filters') || t.closest('.doc-expand-btn') || t.closest('.doc-subfiles')) return;
  }
  document.getElementById(id).classList.toggle('expanded'); 
}
function toggleBlocker(id) { document.getElementById(id).classList.toggle('expanded'); }
function filterDocs(pkgIdx, status, event) {
  event.stopPropagation();
  var list = document.getElementById('doc-list-' + pkgIdx);
  if (!list) return;
  var filters = list.parentElement.querySelector('.doc-filters');
  filters.querySelectorAll('.doc-filter').forEach(function(f) { f.classList.remove('active'); });
  event.target.classList.add('active');
  list.querySelectorAll('.doc-row').forEach(function(row) {
    if (status === 'all') { row.style.display = ''; }
    else { row.style.display = (row.getAttribute('data-docstatus') === status) ? '' : 'none'; }
  });
}

// === PM-EXT TAB (sandbox for experimenting — safe copy) ===
function renderPMExt() {
  if (!selectedProject) return;
  var el = document.getElementById('tc-pm-ext');
  var p = selectedProject;
  var html = '';

  // === Overall project progress ring ===
  var totalPkgs = p.packages.length;
  var completePkgs = p.packages.filter(function(pk){return pk.status==='complete'}).length;
  var activePkgs = p.packages.filter(function(pk){return pk.status==='active'}).length;
  var blockedPkgs = p.packages.filter(function(pk){return pk.status==='blocked'}).length;
  var pendingPkgs = totalPkgs - completePkgs - activePkgs - blockedPkgs;

  html += '<div class="pmx-hero">';
  html += '<div class="pmx-ring-wrap"><svg class="pmx-ring" viewBox="0 0 100 100"><circle cx="50" cy="50" r="42" fill="none" stroke="var(--bg-hover)" stroke-width="8"/><circle cx="50" cy="50" r="42" fill="none" stroke="#4caf50" stroke-width="8" stroke-dasharray="' + (p.progress * 2.64) + ' 264" stroke-linecap="round" transform="rotate(-90 50 50)"/><text x="50" y="46" text-anchor="middle" font-size="18" font-weight="700" fill="var(--text-heading)">' + p.progress + '%</text><text x="50" y="60" text-anchor="middle" font-size="7" fill="var(--text-secondary)">COMPLETE</text></svg></div>';
  html += '<div class="pmx-hero-stats"><div class="pmx-stat"><span class="pmx-stat-val" style="color:#4caf50;">' + completePkgs + '</span><span class="pmx-stat-lbl">Done</span></div><div class="pmx-stat"><span class="pmx-stat-val" style="color:#ff9800;">' + activePkgs + '</span><span class="pmx-stat-lbl">Active</span></div><div class="pmx-stat"><span class="pmx-stat-val" style="color:#f44336;">' + blockedPkgs + '</span><span class="pmx-stat-lbl">Blocked</span></div><div class="pmx-stat"><span class="pmx-stat-val" style="color:#bdbdbd;">' + pendingPkgs + '</span><span class="pmx-stat-lbl">Pending</span></div></div>';
  html += '</div>';

  // === Package timeline / swimlane ===
  html += '<div class="pmx-timeline-title">Package Lifecycle</div>';
  html += '<div class="pmx-timeline">';
  var chainOrder = ['AI-ILC','AI-PILC','AI-POLC','AI-UXD','AI-ADLC','AI-DWG','AI-GCE','AI-TGE'];
  chainOrder.forEach(function(code) {
    var pkg = p.packages.find(function(pk){return pk.code === code});
    if (!pkg) return;
    var pName = (packageNames[code] || code).split(' ')[0];
    var barColor = pkg.status==='complete'?'#4caf50':(pkg.status==='active'?'#ff9800':(pkg.status==='blocked'?'#f44336':'#616161'));
    var emoji = statusEmojis[pkg.status];
    html += '<div class="pmx-lane"><div class="pmx-lane-label"><span class="pmx-lane-code">' + code.replace('AI-','') + '</span><span class="pmx-lane-name">' + pName + '</span></div><div class="pmx-lane-track"><div class="pmx-lane-bar" style="width:' + pkg.progress.pct + '%;background:' + barColor + ';"><span class="pmx-lane-pct">' + (pkg.progress.pct > 15 ? pkg.progress.pct + '%' : '') + '</span></div></div><span class="pmx-lane-emoji">' + emoji + '</span></div>';
  });
  html += '</div>';

  // === Blockers highlight ===
  var allBlockers = [];
  p.packages.forEach(function(pkg) { pkg.blockers.forEach(function(b) { allBlockers.push({ source: pkg.code, text: b }); }); });
  if (allBlockers.length > 0) {
    html += '<div class="pmx-blockers"><div class="pmx-blockers-title">\uD83D\uDEA8 Blockers (' + allBlockers.length + ')</div>';
    allBlockers.forEach(function(b) { html += '<div class="pmx-blocker"><span class="pmx-blocker-src">' + b.source + '</span><span class="pmx-blocker-text">' + b.text + '</span></div>'; });
    html += '</div>';
  }

  // === Artifact completion heatmap ===
  html += '<div class="pmx-heatmap-title">Artifact Heatmap</div>';
  html += '<div class="pmx-heatmap">';
  chainOrder.forEach(function(code) {
    var pkg = p.packages.find(function(pk){return pk.code === code});
    if (!pkg || !pkg.artifacts) return;
    html += '<div class="pmx-heatmap-row"><span class="pmx-heatmap-label">' + code.replace('AI-','') + '</span><div class="pmx-heatmap-cells">';
    pkg.artifacts.forEach(function(a) {
      var color = a.status==='produced'?'#4caf50':(a.status==='in-progress'?'#ff9800':'#333');
      html += '<div class="pmx-cell" style="background:' + color + ';" title="' + a.name + ' (' + a.status + ')"></div>';
    });
    html += '</div></div>';
  });
  html += '</div>';

  // === PM Perspective: DRACIL Summary ===
  var mgmt = p.mgmt || {};
  var mgmtD = p.mgmtDetail || {};
  html += '<div class="pmx-timeline-title">Management Framework (DRACIL)</div>';
  html += '<div class="pmx-dracil">';
  var dracilItems = [
    {key:'decisions',icon:'\uD83D\uDCCB',label:'Decisions',color:'#569cd6'},
    {key:'risks',icon:'\u26A0\uFE0F',label:'Risks',color:'#f44336'},
    {key:'actions',icon:'\u2705',label:'Actions',color:'#4caf50'},
    {key:'changes',icon:'\uD83D\uDD04',label:'Changes',color:'#ff9800'},
    {key:'issues',icon:'\uD83D\uDC1B',label:'Issues',color:'#e91e63'},
    {key:'lessons',icon:'\uD83D\uDCA1',label:'Lessons',color:'#9c27b0'}
  ];
  dracilItems.forEach(function(d) {
    var count = mgmt[d.key] || 0;
    var items = mgmtD[d.key] || [];
    var openCount = items.filter(function(i){var s=(i.status||'').toLowerCase(); return s==='open'||s==='in progress'||s==='pending'||s==='proposed'||s==='investigating'||s==='mitigating';}).length;
    html += '<div class="pmx-dracil-item" style="border-left-color:' + d.color + ';"><div class="pmx-dracil-icon">' + d.icon + '</div><div class="pmx-dracil-body"><div class="pmx-dracil-label">' + d.label + '</div><div class="pmx-dracil-counts"><span class="pmx-dracil-total">' + count + '</span>' + (openCount > 0 ? '<span class="pmx-dracil-open">' + openCount + ' open</span>' : '<span class="pmx-dracil-clear">all clear</span>') + '</div></div></div>';
  });
  html += '</div>';

  // === Critical Path — which package is the bottleneck ===
  html += '<div class="pmx-timeline-title">Critical Path</div>';
  html += '<div class="pmx-critical-path">';
  var criticalPkg = null;
  for (var ci = 0; ci < chainOrder.length; ci++) {
    var cpkg = p.packages.find(function(pk){return pk.code === chainOrder[ci]});
    if (cpkg && (cpkg.status === 'active' || cpkg.status === 'blocked')) { criticalPkg = cpkg; break; }
  }
  if (criticalPkg) {
    var cpColor = criticalPkg.status === 'blocked' ? '#f44336' : '#ff9800';
    var cpName = packageNames[criticalPkg.code] || criticalPkg.code;
    var remaining = criticalPkg.progress.total - criticalPkg.progress.done;
    html += '<div class="pmx-cp-card" style="border-left-color:' + cpColor + ';"><div class="pmx-cp-head"><span class="pmx-cp-code" style="color:' + cpColor + ';">' + criticalPkg.code + '</span><span class="pmx-cp-name">' + cpName + '</span></div>';
    html += '<div class="pmx-cp-detail">Phase ' + criticalPkg.phase.c + '/' + criticalPkg.phase.t + ' \u00B7 ' + criticalPkg.stage.name + '</div>';
    html += '<div class="pmx-cp-detail">' + remaining + ' artifacts remaining \u00B7 ' + criticalPkg.progress.pct + '% complete</div>';
    if (criticalPkg.blockers.length > 0) { html += '<div class="pmx-cp-blocker">\uD83D\uDEA8 ' + criticalPkg.blockers[0] + '</div>'; }
    html += '<div class="pmx-cp-bar"><div class="pmx-cp-bar-fill" style="width:' + criticalPkg.progress.pct + '%;background:' + cpColor + ';"></div></div>';
    html += '</div>';
  } else {
    html += '<div style="font-size:11px;color:#4caf50;padding:8px;">\u2705 No active bottleneck — all packages either complete or pending upstream.</div>';
  }
  html += '</div>';

  // === Dependency Chain Readiness ===
  html += '<div class="pmx-timeline-title">Chain Readiness</div>';
  html += '<div class="pmx-chain-ready">';
  for (var ri = 0; ri < chainOrder.length; ri++) {
    var rpkg = p.packages.find(function(pk){return pk.code === chainOrder[ri]});
    if (!rpkg) continue;
    var rColor = rpkg.status==='complete'?'#4caf50':(rpkg.status==='active'?'#ff9800':(rpkg.status==='blocked'?'#f44336':'#616161'));
    var rReady = rpkg.status === 'complete';
    var nextPkg = (ri < chainOrder.length - 1) ? p.packages.find(function(pk){return pk.code === chainOrder[ri+1]}) : null;
    var handoffReady = rReady && nextPkg && nextPkg.status !== 'complete';
    html += '<div class="pmx-chain-node" style="border-color:' + rColor + ';' + (handoffReady?'box-shadow:0 0 6px '+rColor+'44;':'') + '"><span class="pmx-chain-code" style="color:' + rColor + ';">' + chainOrder[ri].replace('AI-','') + '</span><span class="pmx-chain-status">' + (rpkg.status==='complete'?'\u2705':(rpkg.status==='active'?'\u26A1':(rpkg.status==='blocked'?'\uD83D\uDEAB':'\u23F3'))) + '</span></div>';
    if (ri < chainOrder.length - 1) {
      var arrowColor = rReady ? '#4caf50' : 'var(--border)';
      html += '<div class="pmx-chain-arrow" style="color:' + arrowColor + ';">\u2192</div>';
    }
  }
  html += '</div>';

  el.innerHTML = html;
}

// === PO TAB === (abbreviated — renders vision, roadmap, releases, backlog, acceptance, stakeholders)
function renderPO() {
  if (!selectedProject) return;
  var el = document.getElementById('tc-po');
  var po = selectedProject.po;
  if (!po) { el.innerHTML = '<div class="empty-state">Product ownership data not yet available for this project.</div>'; return; }
  var html = '';

  // === Value Delivery Ring + KPIs (from PO-ext) ===
  var totalStories = po.backlog.totalStories;
  var delivered = 0; ['now','next','later'].forEach(function(h) { (po.roadmap[h]||[]).forEach(function(e){delivered += e.done;}); });
  var deliveredPct = totalStories > 0 ? Math.round(delivered/totalStories*100) : 0;
  var accPct = po.acceptance.totalCriteria>0?Math.round(po.acceptance.validated/po.acceptance.totalCriteria*100):0;
  var velTrend = po.velocity ? po.velocity.trend : 'stable';
  var velIcon = velTrend==='up'?'\u2197\uFE0F':(velTrend==='down'?'\u2198\uFE0F':'\u27A1\uFE0F');

  html += '<div class="pmx-hero">';
  html += '<div class="pmx-ring-wrap"><svg class="pmx-ring" viewBox="0 0 100 100"><circle cx="50" cy="50" r="42" fill="none" stroke="var(--bg-hover)" stroke-width="8"/><circle cx="50" cy="50" r="42" fill="none" stroke="#9c27b0" stroke-width="8" stroke-dasharray="' + (deliveredPct * 2.64) + ' 264" stroke-linecap="round" transform="rotate(-90 50 50)"/><text x="50" y="46" text-anchor="middle" font-size="18" font-weight="700" fill="var(--text-heading)">' + deliveredPct + '%</text><text x="50" y="60" text-anchor="middle" font-size="7" fill="var(--text-secondary)">DELIVERED</text></svg></div>';
  html += '<div class="pmx-hero-stats"><div class="pmx-stat"><span class="pmx-stat-val" style="color:#9c27b0;">' + delivered + '</span><span class="pmx-stat-lbl">Stories Done</span></div><div class="pmx-stat"><span class="pmx-stat-val">' + totalStories + '</span><span class="pmx-stat-lbl">Total</span></div><div class="pmx-stat"><span class="pmx-stat-val" style="color:' + (accPct>=70?'#4caf50':'#ff9800') + ';">' + accPct + '%</span><span class="pmx-stat-lbl">Accepted</span></div><div class="pmx-stat"><span class="pmx-stat-val">' + velIcon + '</span><span class="pmx-stat-lbl">Velocity</span></div></div>';
  html += '</div>';

  // === Roadmap Burndown ===
  html += '<div class="pmx-timeline-title">Roadmap Burndown</div>';
  html += '<div class="pmx-timeline">';
  [{key:'now',label:'NOW',color:'#4caf50'},{key:'next',label:'NEXT',color:'#ff9800'},{key:'later',label:'LATER',color:'#9e9e9e'}].forEach(function(h) {
    var epics = po.roadmap[h.key]||[];
    var totalS = 0, doneS = 0; epics.forEach(function(e){totalS+=e.stories; doneS+=e.done;});
    var pct = totalS>0?Math.round(doneS/totalS*100):0;
    html += '<div class="pmx-lane"><div class="pmx-lane-label"><span class="pmx-lane-code" style="color:' + h.color + ';">' + h.label + '</span><span class="pmx-lane-name">' + epics.length + ' epics</span></div><div class="pmx-lane-track"><div class="pmx-lane-bar" style="width:' + pct + '%;background:' + h.color + ';"><span class="pmx-lane-pct">' + (pct > 10 ? doneS + '/' + totalS : '') + '</span></div></div><span class="pmx-lane-emoji">' + pct + '%</span></div>';
  });
  html += '</div>';

  // === Epic Progress Map ===
  html += '<div class="pmx-timeline-title">Epic Progress Map</div>';
  html += '<div class="pmx-epic-map">';
  ['now','next','later'].forEach(function(h) {
    (po.roadmap[h]||[]).forEach(function(e) {
      var pct = e.stories>0?Math.round(e.done/e.stories*100):0;
      var size = Math.max(40, Math.min(80, e.stories * 3));
      var sc = pct>=80?'#4caf50':(pct>=40?'#2196f3':(pct>0?'#ff9800':'#616161'));
      html += '<div class="pmx-epic-bubble" style="width:' + size + 'px;height:' + size + 'px;border-color:' + sc + ';background:' + sc + '15;"><span class="pmx-epic-bubble-name">' + e.epic.split(' ').slice(0,2).join(' ') + '</span><span class="pmx-epic-bubble-pct" style="color:' + sc + ';">' + pct + '%</span></div>';
    });
  });
  html += '</div>';

  // === Release Countdown ===
  if (po.releases && po.releases.length) {
    html += '<div class="pmx-timeline-title">Release Countdown</div>';
    html += '<div class="pmx-releases-visual">';
    po.releases.forEach(function(r) {
      var pct = r.stories>0?Math.round(r.done/r.stories*100):0;
      var sc = r.status==='in-progress'?'#ff9800':(r.status==='released'?'#4caf50':(r.status==='at-risk'?'#f44336':'#569cd6'));
      var statusIcon = r.status==='released'?'\u2705':(r.status==='in-progress'?'\u26A1':(r.status==='at-risk'?'\uD83D\uDEA8':'\uD83D\uDCC5'));
      html += '<div class="pmx-release-row"><div class="pmx-release-info"><span class="pmx-release-icon" style="color:' + sc + ';">' + statusIcon + '</span><span class="pmx-release-name">' + r.name + '</span><span class="pmx-release-date">' + r.date + '</span></div><div class="pmx-release-bar-wrap"><div class="pmx-lane-track"><div class="pmx-lane-bar" style="width:' + pct + '%;background:' + sc + ';"><span class="pmx-lane-pct">' + (pct > 15 ? pct + '%' : '') + '</span></div></div></div></div>';
    });
    html += '</div>';
  }

  // === Stakeholder Engagement ===
  if (po.stakeholders && po.stakeholders.length) {
    html += '<div class="pmx-timeline-title">Stakeholder Engagement</div>';
    html += '<div class="pmx-stakeholders">';
    po.stakeholders.forEach(function(s) {
      var engColor = s.engagement==='champion'?'#4caf50':(s.engagement==='supportive'?'#2196f3':(s.engagement==='neutral'?'#ff9800':'#f44336'));
      var infSize = s.influence==='high'?'14px':'11px';
      html += '<div class="pmx-stakeholder"><div class="pmx-sh-avatar" style="border-color:' + engColor + ';font-size:' + infSize + ';">\uD83D\uDC64</div><div class="pmx-sh-info"><span class="pmx-sh-name">' + s.name + '</span><span class="pmx-sh-meta"><span style="color:' + engColor + ';">' + s.engagement + '</span> \u00B7 ' + s.influence + '</span></div></div>';
    });
    html += '</div>';
  }


  // === Separator ===
  html += '<div style="border-top:1px solid var(--border);margin:16px 0;"></div>';

  // === Vision ===
  var vc = po.vision.status === 'defined' ? '#4caf50' : '#ff9800';
  html += '<div class="po-vision"><span class="po-badge" style="background:' + vc + '22;color:' + vc + ';border:1px solid ' + vc + '44;">' + po.vision.status + '</span><div class="vision-text">\u201C' + po.vision.statement + '\u201D</div></div>';

  // Roadmap — collapsible, starts open
  html += '<div class="mf-group" id="po-grp-roadmap"><div class="mf-group-hdr" onclick="document.getElementById(\'po-grp-roadmap\').classList.toggle(\'collapsed\')" style="border-left-color:#569cd6;"><span class="mf-grp-arrow">\u25BC</span><span class="mf-grp-icon">\uD83D\uDDFA\uFE0F</span><span class="mf-grp-label">Roadmap</span><span class="mf-grp-count">' + ((po.roadmap.now||[]).length + (po.roadmap.next||[]).length + (po.roadmap.later||[]).length) + ' epics</span></div><div class="mf-group-body">';
  [{key:'now',label:'Now',color:'#4caf50'},{key:'next',label:'Next',color:'#ff9800'},{key:'later',label:'Later',color:'#bdbdbd'}].forEach(function(h) {
    var epics = po.roadmap[h.key]||[];
    if (epics.length === 0) return;
    html += '<div style="margin-bottom:8px;"><span style="font-size:10px;font-weight:700;text-transform:uppercase;color:' + h.color + ';">' + h.label + ' (' + epics.length + ')</span></div>';
    epics.forEach(function(e, ei) {
      var pct = e.stories>0?Math.round(e.done/e.stories*100):0;
      var sc = pct>=80?'#4caf50':(pct>=40?'#2196f3':(pct>0?'#ff9800':'#616161'));
      var epicId = 'po-epic-' + h.key + '-' + ei;
      html += '<div class="mf-item" id="' + epicId + '"><div class="mf-item-hdr" onclick="toggleMfItem(\'' + epicId + '\',event)"><span class="mf-item-dot" style="background:' + sc + ';"></span><span class="mf-item-title">' + e.epic + '</span><span class="mf-item-status" style="color:' + sc + ';">' + e.done + '/' + e.stories + '</span></div>';
      html += '<div class="mf-item-body"><div style="display:flex;justify-content:space-between;font-size:11px;margin-bottom:4px;"><span>Progress: ' + pct + '%</span><span>Status: ' + e.status + '</span></div><div class="progress-bar"><div class="progress-fill ' + (pct>=80?'complete':'active') + '" style="width:' + pct + '%"></div></div>';
      // Sub-items (stories)
      if (e.items && e.items.length > 0) {
        var doneCount = e.items.filter(function(s){return s.status==='done'}).length;
        var ipCount = e.items.filter(function(s){return s.status==='in-progress'}).length;
        var todoCount = e.items.filter(function(s){return s.status==='todo'}).length;
        html += '<div class="po-stories"><div class="po-stories-summary"><span class="po-ss-done">\u2705 ' + doneCount + '</span><span class="po-ss-ip">\uD83D\uDD04 ' + ipCount + '</span><span class="po-ss-todo">\u23F3 ' + todoCount + '</span></div>';
        e.items.forEach(function(s) {
          var sDot = s.status==='done'?'dot-produced':(s.status==='in-progress'?'dot-active':'dot-pending');
          html += '<div class="po-story-row"><span class="doc-dot ' + sDot + '"></span><span>' + s.name + '</span></div>';
        });
        html += '</div>';
      }
      html += '</div></div>';
    });
  });
  html += '</div></div>';

  // Releases — collapsible, starts open
  if (po.releases && po.releases.length) {
    html += '<div class="mf-group" id="po-grp-releases"><div class="mf-group-hdr" onclick="document.getElementById(\'po-grp-releases\').classList.toggle(\'collapsed\')" style="border-left-color:#9c27b0;"><span class="mf-grp-arrow">\u25BC</span><span class="mf-grp-icon">\uD83D\uDE80</span><span class="mf-grp-label">Releases</span><span class="mf-grp-count">' + po.releases.length + '</span></div><div class="mf-group-body">';
    po.releases.forEach(function(r, ri) {
      var pct = r.stories>0?Math.round(r.done/r.stories*100):0;
      var sc = r.status==='in-progress'?'#ff9800':(r.status==='released'?'#4caf50':(r.status==='at-risk'?'#f44336':'#bdbdbd'));
      html += '<div class="mf-item" id="po-rel-' + ri + '"><div class="mf-item-hdr" onclick="toggleMfItem(\'po-rel-' + ri + '\',event)"><span class="mf-item-dot" style="background:' + sc + ';"></span><span class="mf-item-title">' + r.name + '</span><span class="mf-item-status" style="color:' + sc + ';">' + r.status + '</span></div>';
      html += '<div class="mf-item-body"><div class="mf-item-meta"><span>\uD83D\uDCC5 ' + r.date + '</span></div><div style="display:flex;justify-content:space-between;font-size:11px;margin:4px 0;"><span>' + r.done + '/' + r.stories + ' stories</span><span>' + pct + '%</span></div><div class="progress-bar"><div class="progress-fill ' + (pct>=80?'complete':'active') + '" style="width:' + pct + '%"></div></div>';
      // Scope sub-items
      if (r.scope && r.scope.length > 0) {
        html += '<div class="po-stories">';
        r.scope.forEach(function(sg) {
          var sgDot = sg.status==='done'?'dot-produced':(sg.status==='in-progress'?'dot-active':'dot-pending');
          var sgPct = sg.stories>0?Math.round(sg.done/sg.stories*100):0;
          html += '<div class="po-story-row"><span class="doc-dot ' + sgDot + '"></span><span style="flex:1;">' + sg.name + '</span><span style="font-size:10px;color:var(--text-secondary);">' + sg.done + '/' + sg.stories + '</span></div>';
        });
        html += '</div>';
      }
      html += '</div></div>';
    });
    html += '</div></div>';
  }

  // Backlog Health — collapsible, starts collapsed
  html += '<div class="mf-group collapsed" id="po-grp-backlog"><div class="mf-group-hdr" onclick="document.getElementById(\'po-grp-backlog\').classList.toggle(\'collapsed\')" style="border-left-color:#ff9800;"><span class="mf-grp-arrow">\u25BC</span><span class="mf-grp-icon">\uD83D\uDCCB</span><span class="mf-grp-label">Backlog Health</span><span class="mf-grp-status-pills"><span class="mf-grp-spill" style="color:var(--text-secondary);">' + po.backlog.totalEpics + ' epics \u00B7 ' + po.backlog.totalStories + ' stories \u00B7 ' + po.backlog.prioritised + ' prioritised</span></span><span class="mf-grp-count"></span></div><div class="mf-group-body">';
  html += '<div class="mf-summary" style="margin:6px 0;">';
  html += '<div class="mf-kpi"><span class="mf-kpi-val">' + po.backlog.totalEpics + '</span><span class="mf-kpi-lbl">Epics</span></div>';
  html += '<div class="mf-kpi"><span class="mf-kpi-val">' + po.backlog.totalStories + '</span><span class="mf-kpi-lbl">Stories</span></div>';
  html += '<div class="mf-kpi"><span class="mf-kpi-val">' + po.backlog.prioritised + '</span><span class="mf-kpi-lbl">Prioritised</span></div>';
  html += '<div class="mf-kpi"><span class="mf-kpi-val">' + po.backlog.inReleasePlan + '</span><span class="mf-kpi-lbl">In Release</span></div>';
  html += '</div>';
  html += '<div style="margin-top:8px;display:flex;gap:6px;"><span class="po-badge ' + (po.backlog.dorReady?'yes':'no') + '">DoR ' + (po.backlog.dorReady?'\u2713':'\u2717') + '</span><span class="po-badge ' + (po.backlog.dodReady?'yes':'no') + '">DoD ' + (po.backlog.dodReady?'\u2713':'\u2717') + '</span></div>';
  // Prioritisation gauge
  var priPct = po.backlog.totalStories>0?Math.round(po.backlog.prioritised/po.backlog.totalStories*100):0;
  html += '<div class="pmx-health-gauges" style="margin-top:10px;">';
  html += '<div class="pmx-gauge"><svg viewBox="0 0 100 60" class="pmx-gauge-svg"><path d="M10 55 A 40 40 0 0 1 90 55" fill="none" stroke="var(--bg-hover)" stroke-width="8" stroke-linecap="round"/><path d="M10 55 A 40 40 0 0 1 90 55" fill="none" stroke="#9c27b0" stroke-width="8" stroke-linecap="round" stroke-dasharray="' + (priPct * 1.26) + ' 126"/></svg><div class="pmx-gauge-label">' + priPct + '% Prioritised</div></div>';
  html += '</div>';
  html += '</div></div>';

  // Acceptance Criteria — collapsible, starts collapsed
  html += '<div class="mf-group collapsed" id="po-grp-acceptance"><div class="mf-group-hdr" onclick="document.getElementById(\'po-grp-acceptance\').classList.toggle(\'collapsed\')" style="border-left-color:#4caf50;"><span class="mf-grp-arrow">\u25BC</span><span class="mf-grp-icon">\u2705</span><span class="mf-grp-label">Acceptance Criteria</span><span class="mf-grp-status-pills"><span class="mf-grp-spill" style="color:' + (accPct>=70?'#4caf50':'#ff9800') + ';">' + accPct + '% validated</span></span><span class="mf-grp-count">' + po.acceptance.validated + '/' + po.acceptance.totalCriteria + '</span></div><div class="mf-group-body">';
  html += '<div style="padding:8px 0;"><div style="display:flex;justify-content:space-between;font-size:12px;margin-bottom:6px;"><span>Validated</span><span>' + po.acceptance.validated + '/' + po.acceptance.totalCriteria + ' (' + accPct + '%)</span></div><div class="progress-bar"><div class="progress-fill ' + (accPct>=80?'complete':'active') + '" style="width:' + accPct + '%"></div></div></div>';
  html += '</div></div>';

  el.innerHTML = html;
}

// === PO-EXT TAB (Product Owner visual perspective) ===
function renderPOExt() {
  if (!selectedProject) return;
  var el = document.getElementById('tc-po-ext');
  var po = selectedProject.po;
  if (!po) { el.innerHTML = '<div class="empty-state">Product ownership data not yet available.</div>'; return; }
  var html = '';

  // === Value Delivery Scorecard ===
  var totalStories = po.backlog.totalStories;
  var delivered = 0; ['now','next','later'].forEach(function(h) { (po.roadmap[h]||[]).forEach(function(e){delivered += e.done;}); });
  var deliveredPct = totalStories > 0 ? Math.round(delivered/totalStories*100) : 0;
  var accPct = po.acceptance.totalCriteria>0?Math.round(po.acceptance.validated/po.acceptance.totalCriteria*100):0;
  var velTrend = po.velocity ? po.velocity.trend : 'stable';
  var velIcon = velTrend==='up'?'\u2197\uFE0F':(velTrend==='down'?'\u2198\uFE0F':'\u27A1\uFE0F');

  html += '<div class="pmx-hero">';
  html += '<div class="pmx-ring-wrap"><svg class="pmx-ring" viewBox="0 0 100 100"><circle cx="50" cy="50" r="42" fill="none" stroke="var(--bg-hover)" stroke-width="8"/><circle cx="50" cy="50" r="42" fill="none" stroke="#9c27b0" stroke-width="8" stroke-dasharray="' + (deliveredPct * 2.64) + ' 264" stroke-linecap="round" transform="rotate(-90 50 50)"/><text x="50" y="46" text-anchor="middle" font-size="18" font-weight="700" fill="var(--text-heading)">' + deliveredPct + '%</text><text x="50" y="60" text-anchor="middle" font-size="7" fill="var(--text-secondary)">DELIVERED</text></svg></div>';
  html += '<div class="pmx-hero-stats"><div class="pmx-stat"><span class="pmx-stat-val" style="color:#9c27b0;">' + delivered + '</span><span class="pmx-stat-lbl">Stories Done</span></div><div class="pmx-stat"><span class="pmx-stat-val">' + totalStories + '</span><span class="pmx-stat-lbl">Total Backlog</span></div><div class="pmx-stat"><span class="pmx-stat-val" style="color:' + (accPct>=70?'#4caf50':'#ff9800') + ';">' + accPct + '%</span><span class="pmx-stat-lbl">Accepted</span></div><div class="pmx-stat"><span class="pmx-stat-val">' + velIcon + '</span><span class="pmx-stat-lbl">Velocity</span></div></div>';
  html += '</div>';

  // === Roadmap Burndown (visual bars per horizon) ===
  html += '<div class="pmx-timeline-title">Roadmap Burndown</div>';
  html += '<div class="pmx-timeline">';
  [{key:'now',label:'NOW',color:'#4caf50'},{key:'next',label:'NEXT',color:'#ff9800'},{key:'later',label:'LATER',color:'#9e9e9e'}].forEach(function(h) {
    var epics = po.roadmap[h.key]||[];
    var totalS = 0, doneS = 0; epics.forEach(function(e){totalS+=e.stories; doneS+=e.done;});
    var pct = totalS>0?Math.round(doneS/totalS*100):0;
    html += '<div class="pmx-lane"><div class="pmx-lane-label"><span class="pmx-lane-code" style="color:' + h.color + ';">' + h.label + '</span><span class="pmx-lane-name">' + epics.length + ' epics</span></div><div class="pmx-lane-track"><div class="pmx-lane-bar" style="width:' + pct + '%;background:' + h.color + ';"><span class="pmx-lane-pct">' + (pct > 10 ? doneS + '/' + totalS : '') + '</span></div></div><span class="pmx-lane-emoji">' + pct + '%</span></div>';
  });
  html += '</div>';

  // === Release Countdown ===
  if (po.releases && po.releases.length) {
    html += '<div class="pmx-timeline-title">Release Countdown</div>';
    html += '<div class="pmx-releases-visual">';
    po.releases.forEach(function(r) {
      var pct = r.stories>0?Math.round(r.done/r.stories*100):0;
      var sc = r.status==='in-progress'?'#ff9800':(r.status==='released'?'#4caf50':(r.status==='at-risk'?'#f44336':'#569cd6'));
      var statusIcon = r.status==='released'?'\u2705':(r.status==='in-progress'?'\u26A1':(r.status==='at-risk'?'\uD83D\uDEA8':'\uD83D\uDCC5'));
      html += '<div class="pmx-release-row"><div class="pmx-release-info"><span class="pmx-release-icon" style="color:' + sc + ';">' + statusIcon + '</span><span class="pmx-release-name">' + r.name + '</span><span class="pmx-release-date">' + r.date + '</span></div><div class="pmx-release-bar-wrap"><div class="pmx-lane-track"><div class="pmx-lane-bar" style="width:' + pct + '%;background:' + sc + ';"><span class="pmx-lane-pct">' + (pct > 15 ? pct + '%' : '') + '</span></div></div></div></div>';
    });
    html += '</div>';
  }

  // === Epic Value Map (bubble-like visual) ===
  html += '<div class="pmx-timeline-title">Epic Progress Map</div>';
  html += '<div class="pmx-epic-map">';
  ['now','next','later'].forEach(function(h) {
    (po.roadmap[h]||[]).forEach(function(e) {
      var pct = e.stories>0?Math.round(e.done/e.stories*100):0;
      var size = Math.max(40, Math.min(80, e.stories * 3));
      var sc = pct>=80?'#4caf50':(pct>=40?'#2196f3':(pct>0?'#ff9800':'#616161'));
      html += '<div class="pmx-epic-bubble" style="width:' + size + 'px;height:' + size + 'px;border-color:' + sc + ';background:' + sc + '15;"><span class="pmx-epic-bubble-name">' + e.epic.split(' ').slice(0,2).join(' ') + '</span><span class="pmx-epic-bubble-pct" style="color:' + sc + ';">' + pct + '%</span></div>';
    });
  });
  html += '</div>';

  // === Stakeholder Engagement (if data exists) ===
  if (po.stakeholders && po.stakeholders.length) {
    html += '<div class="pmx-timeline-title">Stakeholder Engagement</div>';
    html += '<div class="pmx-stakeholders">';
    po.stakeholders.forEach(function(s) {
      var engColor = s.engagement==='champion'?'#4caf50':(s.engagement==='supportive'?'#2196f3':(s.engagement==='neutral'?'#ff9800':'#f44336'));
      var infSize = s.influence==='high'?'14px':'11px';
      html += '<div class="pmx-stakeholder"><div class="pmx-sh-avatar" style="border-color:' + engColor + ';font-size:' + infSize + ';">\uD83D\uDC64</div><div class="pmx-sh-info"><span class="pmx-sh-name">' + s.name + '</span><span class="pmx-sh-meta"><span style="color:' + engColor + ';">' + s.engagement + '</span> \u00B7 ' + s.influence + ' influence</span></div></div>';
    });
    html += '</div>';
  }

  // === Backlog Health Gauge ===
  html += '<div class="pmx-timeline-title">Backlog Health</div>';
  var dorOk = po.backlog.dorReady;
  var dodOk = po.backlog.dodReady;
  var priPct = po.backlog.totalStories>0?Math.round(po.backlog.prioritised/po.backlog.totalStories*100):0;
  html += '<div class="pmx-health-gauges">';
  html += '<div class="pmx-gauge"><svg viewBox="0 0 100 60" class="pmx-gauge-svg"><path d="M10 55 A 40 40 0 0 1 90 55" fill="none" stroke="var(--bg-hover)" stroke-width="8" stroke-linecap="round"/><path d="M10 55 A 40 40 0 0 1 90 55" fill="none" stroke="#9c27b0" stroke-width="8" stroke-linecap="round" stroke-dasharray="' + (priPct * 1.26) + ' 126"/></svg><div class="pmx-gauge-label">' + priPct + '% Prioritised</div></div>';
  html += '<div class="pmx-gauge-badges"><span class="po-badge ' + (dorOk?'yes':'no') + '">DoR ' + (dorOk?'\u2713':'\u2717') + '</span><span class="po-badge ' + (dodOk?'yes':'no') + '">DoD ' + (dodOk?'\u2713':'\u2717') + '</span></div>';
  html += '</div>';

  el.innerHTML = html;
}

// === ARCHITECT TAB ===
function renderArch() {
  if (!selectedProject) return;
  var el = document.getElementById('tc-architect');
  var arch = selectedProject.arch;
  if (!arch) { el.innerHTML = '<div class="empty-state">Architecture data not yet available for this project.</div>'; return; }
  var html = '';

  // === C4 Model Progress — visual pipeline ===
  var c4Levels = ['context','container','component','code'];
  var c4Done = c4Levels.filter(function(l){return arch.c4Progress[l]==='complete'}).length;
  var c4Total = c4Levels.length;
  html += '<div class="arch-c4-pipeline">';
  c4Levels.forEach(function(l, i) {
    var s = arch.c4Progress[l];
    var cls = s==='complete'?'c4-done':(s==='in-progress'?'c4-active':'c4-pending');
    var icon = s==='complete'?'\u2705':(s==='in-progress'?'\u26A1':'\u25CB');
    html += '<div class="arch-c4-node ' + cls + '"><div class="c4-icon">' + icon + '</div><div class="c4-label">' + l.charAt(0).toUpperCase()+l.slice(1) + '</div></div>';
    if (i < 3) html += '<div class="arch-c4-connector ' + (s==='complete'?'c4-conn-done':'') + '"></div>';
  });
  html += '</div>';
  html += '<div style="text-align:center;font-size:10px;color:var(--text-secondary);margin-bottom:14px;">' + c4Done + '/' + c4Total + ' levels complete</div>';

  // === Architecture Vision ===
  if (arch.vision) {
    var vc = arch.vision.status==='approved'?'#4caf50':'#ff9800';
    html += '<div class="po-vision"><span class="po-badge" style="background:' + vc + '22;color:' + vc + ';border:1px solid ' + vc + '44;">' + (arch.vision.status||'draft') + '</span><div class="vision-text">\u201C' + arch.vision.statement + '\u201D</div>';
    if (arch.vision.optimisesFor && arch.vision.optimisesFor.length) {
      html += '<div style="margin-top:8px;display:flex;flex-wrap:wrap;gap:5px;">';
      arch.vision.optimisesFor.forEach(function(o) { html += '<span class="ux-ds-chip"><span class="ux-ds-chip-dot" style="background:#569cd6;"></span>' + o + '</span>'; });
      html += '</div>';
    }
    if (arch.vision.path) html += '<div style="margin-top:6px;"><a href="#" onclick="openArtifact(\'' + arch.vision.path.replace(/'/g, "\\'") + '\',event);return false;" style="font-size:11px;color:var(--accent);">\uD83D\uDCC4 Open Architecture Vision</a></div>';
    html += '</div>';
  }

  // === Guiding Principles ===
  if ((arch.principles||[]).length > 0) {
    html += '<div class="mf-group" id="arch-grp-principles"><div class="mf-group-hdr" onclick="document.getElementById(\'arch-grp-principles\').classList.toggle(\'collapsed\')" style="border-left-color:#569cd6;"><span class="mf-grp-arrow">\u25BC</span><span class="mf-grp-icon">\uD83C\uDFDB\uFE0F</span><span class="mf-grp-label">Guiding Principles</span><span class="mf-grp-count">' + (arch.principles||[]).length + '</span></div><div class="mf-group-body">';
    html += '<div style="display:flex;flex-wrap:wrap;gap:5px;">';
    (arch.principles||[]).forEach(function(p) {
      html += '<span class="ux-ds-chip" title="' + p.id + ': ' + p.summary + '"><span class="ux-ds-chip-dot" style="background:#569cd6;"></span>' + p.id + ': ' + p.name + '</span>';
    });
    html += '</div></div></div>';
  }

  // === Architecture Health Ring + Stats ===
  var nfrKeys = Object.keys(arch.nfrs);
  var nfrDefined = nfrKeys.filter(function(k){return arch.nfrs[k].defined}).length;
  var nfrTotal = nfrKeys.length;
  var intContracted = arch.integrations.filter(function(i){return i.status==='contracted'}).length;
  var adrAccepted = arch.adrs.filter(function(a){return a.status==='Accepted'}).length;
  var healthScore = Math.round(((c4Done/4)*25 + (nfrTotal>0?(nfrDefined/nfrTotal):0)*25 + (arch.integrations.length>0?(intContracted/arch.integrations.length):0)*25 + (arch.adrs.length>0?(adrAccepted/arch.adrs.length):0)*25));

  html += '<div class="pmx-hero">';
  html += '<div class="pmx-ring-wrap"><svg class="pmx-ring" viewBox="0 0 100 100"><circle cx="50" cy="50" r="42" fill="none" stroke="var(--bg-hover)" stroke-width="8"/><circle cx="50" cy="50" r="42" fill="none" stroke="#569cd6" stroke-width="8" stroke-dasharray="' + (healthScore * 2.64) + ' 264" stroke-linecap="round" transform="rotate(-90 50 50)"/><text x="50" y="46" text-anchor="middle" font-size="18" font-weight="700" fill="var(--text-heading)">' + healthScore + '%</text><text x="50" y="60" text-anchor="middle" font-size="7" fill="var(--text-secondary)">ARCH HEALTH</text></svg></div>';
  html += '<div class="pmx-hero-stats"><div class="pmx-stat"><span class="pmx-stat-val" style="color:#569cd6;">' + c4Done + '/4</span><span class="pmx-stat-lbl">C4 Levels</span></div><div class="pmx-stat"><span class="pmx-stat-val">' + arch.adrs.length + '</span><span class="pmx-stat-lbl">ADRs</span></div><div class="pmx-stat"><span class="pmx-stat-val">' + arch.integrations.length + '</span><span class="pmx-stat-lbl">Integrations</span></div><div class="pmx-stat"><span class="pmx-stat-val" style="color:' + ((arch.risks||[]).length>2?'#f44336':'#4caf50') + ';">' + (arch.risks||[]).length + '</span><span class="pmx-stat-lbl">Risks</span></div></div>';
  html += '</div>';

  // === NFR Radar ===
  var nfrAxes = nfrKeys.map(function(k) { return {label:k.charAt(0).toUpperCase()+k.slice(1,4),val:arch.nfrs[k].defined?100:0}; });
  if (nfrAxes.length >= 3) {
    var ncx=120, ncy=100, nmaxR=70;
    html += '<div class="uxe-radar-card"><div class="pmx-timeline-title" style="margin-top:0;">NFR Coverage Radar</div><svg viewBox="0 0 240 200" class="uxe-radar-svg">';
    [0.5,1].forEach(function(s) { html += '<circle cx="'+ncx+'" cy="'+ncy+'" r="'+(nmaxR*s)+'" fill="none" stroke="var(--border)" stroke-width="0.5" stroke-dasharray="2,2"/>'; });
    nfrAxes.forEach(function(a, i) { var angle=(Math.PI*2/nfrAxes.length)*i-Math.PI/2; var x2=ncx+Math.cos(angle)*nmaxR; var y2=ncy+Math.sin(angle)*nmaxR; var lx=ncx+Math.cos(angle)*(nmaxR+12); var ly=ncy+Math.sin(angle)*(nmaxR+12); html += '<line x1="'+ncx+'" y1="'+ncy+'" x2="'+x2+'" y2="'+y2+'" stroke="var(--border)" stroke-width="0.5"/>'; html += '<text x="'+lx+'" y="'+ly+'" text-anchor="middle" font-size="7" fill="var(--text-secondary)">'+a.label+'</text>'; });
    var nPoints = nfrAxes.map(function(a, i) { var angle=(Math.PI*2/nfrAxes.length)*i-Math.PI/2; var r=nmaxR*(a.val/100); return (ncx+Math.cos(angle)*r)+','+(ncy+Math.sin(angle)*r); }).join(' ');
    html += '<polygon points="'+nPoints+'" fill="#569cd622" stroke="#569cd6" stroke-width="1.5"/>';
    nfrAxes.forEach(function(a, i) { var angle=(Math.PI*2/nfrAxes.length)*i-Math.PI/2; var r=nmaxR*(a.val/100); var c=a.val>0?'#4caf50':'#f44336'; html += '<circle cx="'+(ncx+Math.cos(angle)*r)+'" cy="'+(ncy+Math.sin(angle)*r)+'" r="3" fill="'+c+'"/>'; });
    html += '</svg></div>';
  }

  // === Integration Health Matrix ===
  html += '<div class="pmx-timeline-title">Integration Health</div>';
  html += '<div class="axe-int-matrix">';
  arch.integrations.forEach(function(ig) { var sc = ig.status==='contracted'?'#4caf50':(ig.status==='designed'?'#ff9800':(ig.status==='blocked'?'#f44336':'#616161')); var dirIcon = ig.direction==='inbound'?'\u2B07':(ig.direction==='outbound'?'\u2B06':'\u2194'); html += '<div class="axe-int-card" style="border-left-color:'+sc+';"><div class="axe-int-name">'+ig.name+'</div><div class="axe-int-meta"><span class="axe-int-type">'+ig.type+'</span><span class="axe-int-dir">'+dirIcon+'</span><span class="axe-int-status" style="color:'+sc+';">'+ig.status+'</span></div></div>'; });
  html += '</div>';

  // === Risk Profile Bar ===
  if (arch.risks && arch.risks.length) {
    var rHigh = arch.risks.filter(function(r){return r.severity==='High'}).length;
    var rMed = arch.risks.filter(function(r){return r.severity==='Medium'}).length;
    var rLow = arch.risks.filter(function(r){return r.severity==='Low'}).length;
    var rTotal = arch.risks.length;
    html += '<div class="pmx-timeline-title">Risk Profile</div>';
    html += '<div class="uxe-research-summary"><div class="uxe-impact-bar">';
    if (rHigh) html += '<div class="uxe-impact-seg" style="width:'+(rHigh/rTotal*100)+'%;background:#f44336;"></div>';
    if (rMed) html += '<div class="uxe-impact-seg" style="width:'+(rMed/rTotal*100)+'%;background:#ff9800;"></div>';
    if (rLow) html += '<div class="uxe-impact-seg" style="width:'+(rLow/rTotal*100)+'%;background:#2196f3;"></div>';
    html += '</div><div class="uxe-impact-labels"><span style="color:#f44336;">\u25CF '+rHigh+' High</span><span style="color:#ff9800;">\u25CF '+rMed+' Medium</span><span style="color:#2196f3;">\u25CF '+rLow+' Low</span></div></div>';
  }

  // === Separator ===
  html += '<div style="border-top:1px solid var(--border);margin:16px 0;"></div>';

  // === Architecture Diagrams (C4 L1/L2/L3) — collapsible, lazy mermaid ===
  if (arch.c4Diagrams) {
    var c4diags = [
      {key:'l1', label:'C4 L1 — System Context', color:'#4caf50'},
      {key:'l2', label:'C4 L2 — Container Diagram', color:'#2196f3'},
      {key:'l3', label:'C4 L3 — Component Design', color:'#9c27b0'}
    ];
    var hasC4 = c4diags.some(function(dd){ return arch.c4Diagrams[dd.key] && arch.c4Diagrams[dd.key].mermaid; });
    if (hasC4) {
      html += '<div class="mf-group" id="arch-grp-c4diagrams"><div class="mf-group-hdr" onclick="document.getElementById(\'arch-grp-c4diagrams\').classList.toggle(\'collapsed\')" style="border-left-color:#2196f3;"><span class="mf-grp-arrow">\u25BC</span><span class="mf-grp-icon">\uD83D\uDCC0</span><span class="mf-grp-label">Architecture Diagrams</span><span class="mf-grp-count">7</span></div><div class="mf-group-body">';
      c4diags.forEach(function(dd) {
        var diag = arch.c4Diagrams[dd.key];
        if (!diag || !diag.mermaid) return;
        var mid = 'arch-c4-' + dd.key;
        html += '<div class="mf-group collapsed" id="' + mid + '-grp" style="margin-bottom:8px;"><div class="mf-group-hdr" onclick="document.getElementById(\'' + mid + '-grp\').classList.toggle(\'collapsed\');renderFlowMermaid(\'' + mid + '\')" style="border-left-color:' + dd.color + ';padding:4px 8px;"><span class="mf-grp-arrow">\u25BC</span><span class="mf-grp-label" style="font-size:11px;">' + dd.label + '</span>' + (diag.path ? '<a class="mf-item-link" href="#" onclick="openArtifact(\'' + diag.path.replace(/'/g, "\\'") + '\',event);return false;" style="margin-left:auto;">\uD83D\uDCC4</a>' : '') + '</div><div class="mf-group-body"><div id="' + mid + '" class="arch-diagram-box" data-mermaid="' + encodeURIComponent(diag.mermaid) + '" style="min-height:80px;padding:8px;"></div></div></div>';
      });
      // additional architecture views (security, data, api, infrastructure)
      if (arch.diagrams) {
        var extraViews = [
          {key:'security', label:'Security Architecture', color:'#f44336'},
          {key:'data', label:'Data Architecture', color:'#ff9800'},
          {key:'api', label:'API Architecture', color:'#4caf50'},
          {key:'infrastructure', label:'Integration & Infrastructure', color:'#9c27b0'}
        ];
        extraViews.forEach(function(dd) {
          var diag = arch.diagrams[dd.key];
          if (!diag || !diag.mermaid) return;
          var mid = 'arch-view-' + dd.key;
          html += '<div class="mf-group collapsed" id="' + mid + '-grp" style="margin-bottom:8px;"><div class="mf-group-hdr" onclick="document.getElementById(\'' + mid + '-grp\').classList.toggle(\'collapsed\');renderFlowMermaid(\'' + mid + '\')" style="border-left-color:' + dd.color + ';padding:4px 8px;"><span class="mf-grp-arrow">\u25BC</span><span class="mf-grp-label" style="font-size:11px;">' + dd.label + '</span>' + (diag.path ? '<a class="mf-item-link" href="#" onclick="openArtifact(\'' + diag.path.replace(/'/g, "\\'") + '\',event);return false;" style="margin-left:auto;">\uD83D\uDCC4</a>' : '') + '</div><div class="mf-group-body"><div id="' + mid + '" class="arch-diagram-box" data-mermaid="' + encodeURIComponent(diag.mermaid) + '" style="min-height:80px;padding:8px;"></div></div></div>';
        });
      }
      html += '</div></div>';
    }
  }

  // === ADRs — collapsible, expandable items with file links ===
  var adrAccepted = arch.adrs.filter(function(a){return a.status==='Accepted'}).length;
  var adrProposed = arch.adrs.filter(function(a){return a.status==='Proposed'}).length;
  html += '<div class="mf-group" id="arch-grp-adrs"><div class="mf-group-hdr" onclick="document.getElementById(\'arch-grp-adrs\').classList.toggle(\'collapsed\')" style="border-left-color:#569cd6;"><span class="mf-grp-arrow">\u25BC</span><span class="mf-grp-icon">\uD83D\uDCDC</span><span class="mf-grp-label">Architecture Decisions</span><span class="mf-grp-status-pills"><span class="mf-grp-spill" style="color:#4caf50;">' + adrAccepted + ' accepted</span><span class="mf-grp-spill" style="color:#ff9800;">' + adrProposed + ' proposed</span></span><span class="mf-grp-count">' + arch.adrs.length + '</span></div><div class="mf-group-body">';
  arch.adrs.forEach(function(a, ai) {
    var sc = a.status==='Accepted'?'#4caf50':(a.status==='Proposed'?'#ff9800':'#9e9e9e');
    html += '<div class="mf-item" id="arch-adr-' + ai + '"><div class="mf-item-hdr" onclick="toggleMfItem(\'arch-adr-' + ai + '\',event)"><span class="mf-item-dot" style="background:' + sc + ';"></span><span class="mf-item-id">' + a.id + '</span><span class="mf-item-title">' + a.title + '</span><span class="mf-item-status" style="color:' + sc + ';">' + a.status + '</span>' + (a.path?'<a class="mf-item-link" href="#" onclick="openArtifact(\''+a.path+'\',event);return false;">\uD83D\uDCC4</a>':'') + '</div>';
    html += '<div class="mf-item-body">';
    if (a.context) html += '<div class="mf-item-desc">' + a.context + '</div>';
    html += '<div class="mf-item-meta"><span>\uD83D\uDCC5 ' + a.date + '</span></div>';
    if (a.path) html += '<div class="mf-item-file"><a href="#" onclick="openArtifact(\''+a.path+'\',event);return false;">\uD83D\uDCC4 ' + a.path + '</a></div>';
    html += '</div></div>';
  });
  html += '</div></div>';

  // === ADR Decision Timeline ===
  html += '<div class="pmx-timeline-title">Decision Timeline</div>';
  html += '<div class="axe-timeline">';
  var sortedAdrs = arch.adrs.slice().sort(function(a,b){ return a.date>b.date?1:-1; });
  sortedAdrs.forEach(function(a, i) { var sc = a.status==='Accepted'?'#4caf50':'#ff9800'; html += '<div class="axe-tl-item"><div class="axe-tl-dot" style="background:'+sc+';"></div><div class="axe-tl-line"' + (i===sortedAdrs.length-1?' style="display:none;"':'') + '></div><div class="axe-tl-content"><span class="axe-tl-date">'+a.date+'</span><span class="axe-tl-title">'+a.title+'</span><span class="axe-tl-status" style="color:'+sc+';">'+a.status+'</span></div></div>'; });
  html += '</div>';

  // === Tech Stack — collapsible, visual grouped badges ===
  var stackColors = {languages:'#569cd6',frameworks:'#4caf50',databases:'#ff9800',infrastructure:'#9c27b0',messaging:'#e91e63',observability:'#2196f3'};
  var stackIcons = {languages:'\uD83D\uDCDD',frameworks:'\u2699\uFE0F',databases:'\uD83D\uDDC4\uFE0F',infrastructure:'\u2601\uFE0F',messaging:'\uD83D\uDCE8',observability:'\uD83D\uDD2D'};
  var stackLabels = {languages:'Languages',frameworks:'Frameworks',databases:'Data Stores',infrastructure:'Infrastructure',messaging:'Messaging',observability:'Observability'};
  var totalTech = 0; Object.keys(arch.techStack).forEach(function(g){totalTech += (arch.techStack[g]||[]).length;});
  html += '<div class="mf-group" id="arch-grp-stack"><div class="mf-group-hdr" onclick="document.getElementById(\'arch-grp-stack\').classList.toggle(\'collapsed\')" style="border-left-color:#9c27b0;"><span class="mf-grp-arrow">\u25BC</span><span class="mf-grp-icon">\uD83D\uDEE0\uFE0F</span><span class="mf-grp-label">Technology Stack</span><span class="mf-grp-status-pills"><span class="mf-grp-spill" style="color:var(--text-secondary);">' + totalTech + ' technologies</span></span><span class="mf-grp-count">' + Object.keys(arch.techStack).length + ' layers</span></div><div class="mf-group-body">';
  Object.keys(arch.techStack).forEach(function(g) {
    var items = arch.techStack[g]; if (!items||!items.length) return;
    var c = stackColors[g]||'var(--color-accent)';
    var icon = stackIcons[g]||'\u2022';
    html += '<div class="arch-stack-row"><span class="arch-stack-icon" style="color:'+c+';">'+icon+'</span><span class="arch-stack-cat">'+stackLabels[g]+'</span><span class="arch-stack-tags">';
    items.forEach(function(t) { html += '<span class="arch-tag" style="border-color:'+c+';color:'+c+';">'+t+'</span>'; });
    html += '</span></div>';
  });
  html += '</div></div>';

  // === Integrations — collapsible, expandable items ===
  var intContracted = arch.integrations.filter(function(i){return i.status==='contracted'}).length;
  var intDesigned = arch.integrations.filter(function(i){return i.status==='designed'}).length;
  var intPlanned = arch.integrations.filter(function(i){return i.status==='planned'}).length;
  html += '<div class="mf-group collapsed" id="arch-grp-int"><div class="mf-group-hdr" onclick="document.getElementById(\'arch-grp-int\').classList.toggle(\'collapsed\')" style="border-left-color:#e91e63;"><span class="mf-grp-arrow">\u25BC</span><span class="mf-grp-icon">\uD83D\uDD17</span><span class="mf-grp-label">Integrations</span><span class="mf-grp-status-pills"><span class="mf-grp-spill" style="color:#4caf50;">' + intContracted + ' contracted</span><span class="mf-grp-spill" style="color:#ff9800;">' + intDesigned + ' designed</span><span class="mf-grp-spill" style="color:#bdbdbd;">' + intPlanned + ' planned</span></span><span class="mf-grp-count">' + arch.integrations.length + '</span></div><div class="mf-group-body">';
  arch.integrations.forEach(function(ig, ii) {
    var sc = ig.status==='contracted'?'#4caf50':(ig.status==='designed'?'#ff9800':(ig.status==='blocked'?'#f44336':'#bdbdbd'));
    var di = ig.direction==='inbound'?'\u2B07':(ig.direction==='outbound'?'\u2B06':'\u2194');
    html += '<div class="mf-item" id="arch-int-' + ii + '"><div class="mf-item-hdr" onclick="toggleMfItem(\'arch-int-' + ii + '\',event)"><span class="mf-item-dot" style="background:' + sc + ';"></span><span class="mf-item-id" style="min-width:40px;">' + ig.type + '</span><span class="mf-item-title">' + ig.name + '</span><span class="mf-item-status" style="color:' + sc + ';">' + di + ' ' + ig.status + '</span></div>';
    html += '<div class="mf-item-body"><div class="mf-item-meta"><span>Protocol: ' + ig.type + '</span><span style="margin-left:12px;">Direction: ' + (ig.direction||'unknown') + '</span></div>';
    if (ig.path) html += '<div class="mf-item-file"><a href="#" onclick="openArtifact(\''+ig.path+'\',event);return false;">\uD83D\uDCC4 ' + ig.path + '</a></div>';
    html += '</div></div>';
  });
  html += '</div></div>';

  // === NFRs — collapsible, visual grid with defined/undefined indicator ===
  var nfrKeys = Object.keys(arch.nfrs);
  var nfrDefined = nfrKeys.filter(function(k){return arch.nfrs[k].defined}).length;
  html += '<div class="mf-group collapsed" id="arch-grp-nfr"><div class="mf-group-hdr" onclick="document.getElementById(\'arch-grp-nfr\').classList.toggle(\'collapsed\')" style="border-left-color:#2196f3;"><span class="mf-grp-arrow">\u25BC</span><span class="mf-grp-icon">\uD83C\uDFAF</span><span class="mf-grp-label">Non-Functional Requirements</span><span class="mf-grp-status-pills"><span class="mf-grp-spill" style="color:#4caf50;">' + nfrDefined + ' defined</span><span class="mf-grp-spill" style="color:#ff9800;">' + (nfrKeys.length - nfrDefined) + ' pending</span></span><span class="mf-grp-count">' + nfrKeys.length + '</span></div><div class="mf-group-body">';
  nfrKeys.forEach(function(k) {
    var n = arch.nfrs[k];
    var dotCls = n.defined ? 'dot-produced' : 'dot-pending';
    var label = k.replace(/-/g,' ').replace(/\b\w/g, function(c){return c.toUpperCase();});
    html += '<div class="mf-item"><div class="mf-item-hdr" style="cursor:default;"><span class="doc-dot ' + dotCls + '"></span><span class="mf-item-title" style="text-transform:capitalize;">' + label + '</span><span class="mf-item-status" style="color:' + (n.defined?'#4caf50':'#ff9800') + ';">' + (n.defined?'defined':'pending') + '</span></div>';
    if (n.defined && n.target) html += '<div style="padding:2px 0 4px 21px;font-size:10px;color:var(--text-secondary);">\uD83C\uDFAF ' + n.target + '</div>';
    html += '</div>';
  });
  html += '</div></div>';

  // === Technical Risks — collapsible, severity-ordered ===
  if (arch.risks && arch.risks.length) {
    var rHigh = arch.risks.filter(function(r){return r.severity==='High'}).length;
    var rMed = arch.risks.filter(function(r){return r.severity==='Medium'}).length;
    var rLow = arch.risks.filter(function(r){return r.severity==='Low'}).length;
    html += '<div class="mf-group collapsed" id="arch-grp-risks"><div class="mf-group-hdr" onclick="document.getElementById(\'arch-grp-risks\').classList.toggle(\'collapsed\')" style="border-left-color:#f44336;"><span class="mf-grp-arrow">\u25BC</span><span class="mf-grp-icon">\u26A0\uFE0F</span><span class="mf-grp-label">Technical Risks</span><span class="mf-grp-status-pills"><span class="mf-grp-spill" style="color:#f44336;">' + rHigh + ' high</span><span class="mf-grp-spill" style="color:#ff9800;">' + rMed + ' medium</span><span class="mf-grp-spill" style="color:#bdbdbd;">' + rLow + ' low</span></span><span class="mf-grp-count">' + (arch.risks||[]).length + '</span></div><div class="mf-group-body">';
    var sevOrder = ['High','Medium','Low'];
    sevOrder.forEach(function(sev) {
      arch.risks.filter(function(r){return r.severity===sev}).forEach(function(r) {
        var rc = sev==='High'?'#f44336':(sev==='Medium'?'#ff9800':'#bdbdbd');
        html += '<div class="mf-item"><div class="mf-item-hdr" style="cursor:default;"><span class="mf-item-dot" style="background:' + rc + ';"></span><span class="mf-item-title">' + r.text + '</span><span class="mf-item-status" style="color:' + rc + ';">' + sev + '</span></div></div>';
      });
    });
    html += '</div></div>';
  }

  el.innerHTML = html;
  // Render Mermaid diagrams after DOM is updated
  setTimeout(function() { renderArchDiagrams(arch); }, 50);
}

function renderArchDiagrams(arch) {
  if (typeof mermaid === 'undefined') return;
  var theme = document.documentElement.getAttribute('data-theme') === 'light' ? 'default' : 'dark';
  mermaid.initialize({startOnLoad:false, theme:theme, flowchart:{useMaxWidth:true, curve:'basis'}, securityLevel:'loose'});

  // Container Diagram
  var containerEl = document.getElementById('arch-mermaid-container');
  if (containerEl && arch.techStack) {
    var lines = ['graph TB'];
    lines.push('  subgraph Client["Client Layer"]');
    lines.push('    WEB["Web App"]');
    lines.push('    MOB["Mobile App"]');
    lines.push('  end');
    lines.push('  subgraph API["API Gateway"]');
    lines.push('    GW["API Gateway"]');
    lines.push('  end');
    lines.push('  subgraph Services["Application Services"]');
    var fws = arch.techStack.frameworks || [];
    fws.forEach(function(fw, i) { lines.push('    SVC' + i + '["' + fw.replace(/"/g,"'") + '"]'); });
    lines.push('  end');
    lines.push('  subgraph Data["Data Layer"]');
    var dbs = arch.techStack.databases || [];
    dbs.forEach(function(db, i) { lines.push('    DB' + i + '[("' + db.replace(/"/g,"'") + '")]'); });
    lines.push('  end');
    lines.push('  subgraph Infra["Infrastructure"]');
    var infra = arch.techStack.infrastructure || [];
    infra.forEach(function(inf, i) { lines.push('    INF' + i + '{{"' + inf.replace(/"/g,"'") + '"}}'); });
    lines.push('  end');
    if (arch.techStack.messaging && arch.techStack.messaging.length) {
      lines.push('  subgraph Messaging["Messaging"]');
      arch.techStack.messaging.forEach(function(m, i) { lines.push('    MSG' + i + '>"' + m.replace(/"/g,"'") + '"]'); });
      lines.push('  end');
    }
    if (arch.techStack.observability && arch.techStack.observability.length) {
      lines.push('  subgraph Observability["Observability"]');
      arch.techStack.observability.forEach(function(o, i) { lines.push('    OBS' + i + '("' + o.replace(/"/g,"'") + '")'); });
      lines.push('  end');
    }
    // Connections
    lines.push('  WEB --> GW');
    lines.push('  MOB --> GW');
    fws.forEach(function(fw, i) { lines.push('  GW --> SVC' + i); });
    fws.forEach(function(fw, i) { dbs.forEach(function(db, j) { if (j <= i) lines.push('  SVC' + i + ' --> DB' + j); }); });
    if (arch.techStack.messaging) { fws.forEach(function(fw, i) { lines.push('  SVC' + i + ' -.-> MSG0'); }); }
    // Styles
    lines.push('  style Client fill:#569cd622,stroke:#569cd6');
    lines.push('  style Services fill:#4caf5022,stroke:#4caf50');
    lines.push('  style Data fill:#ff980022,stroke:#ff9800');
    lines.push('  style Infra fill:#9c27b022,stroke:#9c27b0');
    if (arch.techStack.messaging) lines.push('  style Messaging fill:#e91e6322,stroke:#e91e63');
    if (arch.techStack.observability) lines.push('  style Observability fill:#2196f322,stroke:#2196f3');

    containerEl.removeAttribute('data-processed');
    containerEl.innerHTML = '<div class="mermaid">' + lines.join('\n') + '</div>';
    try { mermaid.init(undefined, containerEl.querySelector('.mermaid')); } catch(e) {}
  }

  // Integration Topology
  var intEl = document.getElementById('arch-mermaid-integrations');
  if (intEl && arch.integrations && arch.integrations.length) {
    var iLines = ['graph LR'];
    iLines.push('  APP(("Our System"))');
    arch.integrations.forEach(function(ig, i) {
      var nodeId = 'EXT' + i;
      var safeName = ig.name.replace(/"/g, "'");
      var safeType = ig.type.replace(/"/g, "'").replace(/\//g, "-");
      if (ig.status === 'contracted') {
        iLines.push('  ' + nodeId + '["' + safeName + '"]');
      } else {
        iLines.push('  ' + nodeId + '("' + safeName + '")');
      }
      if (ig.direction === 'inbound') {
        iLines.push('  ' + nodeId + ' -->|"' + safeType + '"| APP');
      } else if (ig.direction === 'outbound') {
        iLines.push('  APP -->|"' + safeType + '"| ' + nodeId);
      } else {
        iLines.push('  APP <-->|"' + safeType + '"| ' + nodeId);
      }
      var sc = ig.status==='contracted'?'#4caf50':(ig.status==='designed'?'#ff9800':'#bdbdbd');
      iLines.push('  style ' + nodeId + ' fill:' + sc + '22,stroke:' + sc);
    });
    iLines.push('  style APP fill:#569cd633,stroke:#569cd6,stroke-width:3px');

    intEl.removeAttribute('data-processed');
    intEl.innerHTML = '<div class="mermaid">' + iLines.join('\n') + '</div>';
    try { mermaid.init(undefined, intEl.querySelector('.mermaid')); } catch(e) {}
  }
}

var archTf = {};
function archGetTf(id) { if (!archTf[id]) archTf[id] = {s:1, x:0, y:0}; return archTf[id]; }
function archApplyTf(id) {
  var box = document.getElementById(id);
  if (!box) return;
  var m = box.querySelector('.mermaid');
  if (!m) return;
  var t = archGetTf(id);
  m.style.transformOrigin = 'top left';
  m.style.transform = 'translate(' + t.x + 'px,' + t.y + 'px) scale(' + t.s + ')';
}
function archZoom(boxId, dir, evt) {
  if (evt) evt.stopPropagation();
  var t = archGetTf(boxId);
  if (dir === 0) { t.s = 1; t.x = 0; t.y = 0; }
  else { t.s = Math.max(0.4, Math.min(4, t.s + dir * 0.25)); }
  archApplyTf(boxId);
}
function archEnableMouse(boxId) {
  var box = document.getElementById(boxId);
  if (!box || box.getAttribute('data-mouse')) return;
  box.setAttribute('data-mouse', '1');
  box.style.cursor = 'grab';
  box.addEventListener('wheel', function(e) {
    e.preventDefault();
    var t = archGetTf(boxId);
    t.s = Math.max(0.4, Math.min(4, t.s + (e.deltaY < 0 ? 0.15 : -0.15)));
    archApplyTf(boxId);
  }, {passive:false});
  var drag = false, sx = 0, sy = 0, ox = 0, oy = 0;
  box.addEventListener('mousedown', function(e) {
    drag = true; sx = e.clientX; sy = e.clientY;
    var t = archGetTf(boxId); ox = t.x; oy = t.y;
    box.style.cursor = 'grabbing'; e.preventDefault();
  });
  window.addEventListener('mousemove', function(e) {
    if (!drag) return;
    var t = archGetTf(boxId);
    t.x = ox + (e.clientX - sx); t.y = oy + (e.clientY - sy);
    archApplyTf(boxId);
  });
  window.addEventListener('mouseup', function() {
    if (drag) { drag = false; box.style.cursor = 'grab'; }
  });
}

// === ARCH-EXT TAB (Architect visual cockpit) ===
function renderArchExt() {
  if (!selectedProject) return;
  var el = document.getElementById('tc-arch-ext');
  var arch = selectedProject.arch;
  if (!arch) { el.innerHTML = '<div class="empty-state">Architecture data not yet available.</div>'; return; }
  var html = '';

  // === Architecture Health Score ===
  var c4Done = ['context','container','component','code'].filter(function(l){return arch.c4Progress[l]==='complete'}).length;
  var nfrDefined = Object.keys(arch.nfrs).filter(function(k){return arch.nfrs[k].defined}).length;
  var nfrTotal = Object.keys(arch.nfrs).length;
  var intContracted = arch.integrations.filter(function(i){return i.status==='contracted'}).length;
  var adrAccepted = arch.adrs.filter(function(a){return a.status==='Accepted'}).length;
  var healthScore = Math.round(((c4Done/4)*25 + (nfrTotal>0?(nfrDefined/nfrTotal):0)*25 + (arch.integrations.length>0?(intContracted/arch.integrations.length):0)*25 + (arch.adrs.length>0?(adrAccepted/arch.adrs.length):0)*25));

  html += '<div class="pmx-hero">';
  html += '<div class="pmx-ring-wrap"><svg class="pmx-ring" viewBox="0 0 100 100"><circle cx="50" cy="50" r="42" fill="none" stroke="var(--bg-hover)" stroke-width="8"/><circle cx="50" cy="50" r="42" fill="none" stroke="#569cd6" stroke-width="8" stroke-dasharray="' + (healthScore * 2.64) + ' 264" stroke-linecap="round" transform="rotate(-90 50 50)"/><text x="50" y="46" text-anchor="middle" font-size="18" font-weight="700" fill="var(--text-heading)">' + healthScore + '%</text><text x="50" y="60" text-anchor="middle" font-size="7" fill="var(--text-secondary)">ARCH HEALTH</text></svg></div>';
  html += '<div class="pmx-hero-stats"><div class="pmx-stat"><span class="pmx-stat-val" style="color:#569cd6;">' + c4Done + '/4</span><span class="pmx-stat-lbl">C4 Levels</span></div><div class="pmx-stat"><span class="pmx-stat-val">' + arch.adrs.length + '</span><span class="pmx-stat-lbl">ADRs</span></div><div class="pmx-stat"><span class="pmx-stat-val">' + arch.integrations.length + '</span><span class="pmx-stat-lbl">Integrations</span></div><div class="pmx-stat"><span class="pmx-stat-val" style="color:' + ((arch.risks||[]).length>2?'#f44336':'#4caf50') + ';">' + (arch.risks||[]).length + '</span><span class="pmx-stat-lbl">Risks</span></div></div>';
  html += '</div>';

  // === NFR Radar Chart ===
  var nfrKeys = Object.keys(arch.nfrs);
  var nfrAxes = nfrKeys.map(function(k) { return {label:k.charAt(0).toUpperCase()+k.slice(1,4),val:arch.nfrs[k].defined?100:0}; });
  if (nfrAxes.length >= 3) {
    var ncx=120, ncy=100, nmaxR=70;
    html += '<div class="uxe-radar-card"><div class="pmx-timeline-title" style="margin-top:0;">NFR Coverage Radar</div><svg viewBox="0 0 240 200" class="uxe-radar-svg">';
    [0.5,1].forEach(function(s) { html += '<circle cx="'+ncx+'" cy="'+ncy+'" r="'+(nmaxR*s)+'" fill="none" stroke="var(--border)" stroke-width="0.5" stroke-dasharray="2,2"/>'; });
    nfrAxes.forEach(function(a, i) {
      var angle = (Math.PI*2/nfrAxes.length)*i - Math.PI/2;
      var x2 = ncx + Math.cos(angle)*nmaxR; var y2 = ncy + Math.sin(angle)*nmaxR;
      var lx = ncx + Math.cos(angle)*(nmaxR+12); var ly = ncy + Math.sin(angle)*(nmaxR+12);
      html += '<line x1="'+ncx+'" y1="'+ncy+'" x2="'+x2+'" y2="'+y2+'" stroke="var(--border)" stroke-width="0.5"/>';
      html += '<text x="'+lx+'" y="'+ly+'" text-anchor="middle" font-size="7" fill="var(--text-secondary)">'+a.label+'</text>';
    });
    var nPoints = nfrAxes.map(function(a, i) { var angle=(Math.PI*2/nfrAxes.length)*i-Math.PI/2; var r=nmaxR*(a.val/100); return (ncx+Math.cos(angle)*r)+','+(ncy+Math.sin(angle)*r); }).join(' ');
    html += '<polygon points="'+nPoints+'" fill="#569cd622" stroke="#569cd6" stroke-width="1.5"/>';
    nfrAxes.forEach(function(a, i) { var angle=(Math.PI*2/nfrAxes.length)*i-Math.PI/2; var r=nmaxR*(a.val/100); var c=a.val>0?'#4caf50':'#f44336'; html += '<circle cx="'+(ncx+Math.cos(angle)*r)+'" cy="'+(ncy+Math.sin(angle)*r)+'" r="3" fill="'+c+'"/>'; });
    html += '</svg><div class="uxe-radar-legend">';
    nfrKeys.forEach(function(k) { var n=arch.nfrs[k]; var c=n.defined?'#4caf50':'#f44336'; html += '<span class="uxe-radar-item"><span style="color:'+c+';font-weight:700;">'+(n.defined?'\u2705':'\u2717')+'</span> '+k+'</span>'; });
    html += '</div></div>';
  }

  // === ADR Decision Timeline ===
  html += '<div class="pmx-timeline-title">Decision Timeline</div>';
  html += '<div class="axe-timeline">';
  var sortedAdrs = arch.adrs.slice().sort(function(a,b){ return a.date>b.date?1:-1; });
  sortedAdrs.forEach(function(a, i) {
    var sc = a.status==='Accepted'?'#4caf50':'#ff9800';
    html += '<div class="axe-tl-item"><div class="axe-tl-dot" style="background:'+sc+';"></div><div class="axe-tl-line"' + (i===sortedAdrs.length-1?' style="display:none;"':'') + '></div><div class="axe-tl-content"><span class="axe-tl-date">'+a.date+'</span><span class="axe-tl-title">'+a.title+'</span><span class="axe-tl-status" style="color:'+sc+';">'+a.status+'</span></div></div>';
  });
  html += '</div>';

  // === Integration Health Matrix ===
  html += '<div class="pmx-timeline-title">Integration Health</div>';
  html += '<div class="axe-int-matrix">';
  var intStatuses = {contracted:'#4caf50',designed:'#ff9800',planned:'#616161',blocked:'#f44336'};
  arch.integrations.forEach(function(ig) {
    var sc = intStatuses[ig.status]||'#616161';
    var dirIcon = ig.direction==='inbound'?'\u2B07':(ig.direction==='outbound'?'\u2B06':'\u2194');
    html += '<div class="axe-int-card" style="border-left-color:'+sc+';"><div class="axe-int-name">'+ig.name+'</div><div class="axe-int-meta"><span class="axe-int-type">'+ig.type+'</span><span class="axe-int-dir">'+dirIcon+'</span><span class="axe-int-status" style="color:'+sc+';">'+ig.status+'</span></div></div>';
  });
  html += '</div>';

  // === Tech Stack Layer Visualization ===
  var stackColors = {languages:'#569cd6',frameworks:'#4caf50',databases:'#ff9800',infrastructure:'#9c27b0',messaging:'#e91e63',observability:'#2196f3'};
  var stackIcons = {languages:'\uD83D\uDCDD',frameworks:'\u2699\uFE0F',databases:'\uD83D\uDDC4\uFE0F',infrastructure:'\u2601\uFE0F',messaging:'\uD83D\uDCE8',observability:'\uD83D\uDD2D'};
  html += '<div class="pmx-timeline-title">Tech Stack Layers</div>';
  html += '<div class="axe-stack-visual">';
  Object.keys(arch.techStack).forEach(function(g) {
    var items = arch.techStack[g]; if (!items||!items.length) return;
    var c = stackColors[g]||'#888'; var icon = stackIcons[g]||'\u2022';
    html += '<div class="axe-stack-layer" style="border-color:'+c+';"><div class="axe-stack-hdr"><span>'+icon+' '+g+'</span><span class="axe-stack-count">'+items.length+'</span></div><div class="axe-stack-items">';
    items.forEach(function(t) { html += '<span class="axe-stack-chip" style="border-color:'+c+';color:'+c+';">'+t+'</span>'; });
    html += '</div></div>';
  });
  html += '</div>';

  // === Risk Severity Gauge ===
  if (arch.risks && arch.risks.length) {
    var rHigh = arch.risks.filter(function(r){return r.severity==='High'}).length;
    var rMed = arch.risks.filter(function(r){return r.severity==='Medium'}).length;
    var rLow = arch.risks.filter(function(r){return r.severity==='Low'}).length;
    var rTotal = arch.risks.length;
    html += '<div class="pmx-timeline-title">Risk Profile</div>';
    html += '<div class="uxe-research-summary"><div class="uxe-impact-bar">';
    if (rHigh) html += '<div class="uxe-impact-seg" style="width:'+(rHigh/rTotal*100)+'%;background:#f44336;"></div>';
    if (rMed) html += '<div class="uxe-impact-seg" style="width:'+(rMed/rTotal*100)+'%;background:#ff9800;"></div>';
    if (rLow) html += '<div class="uxe-impact-seg" style="width:'+(rLow/rTotal*100)+'%;background:#2196f3;"></div>';
    html += '</div><div class="uxe-impact-labels"><span style="color:#f44336;">\u25CF '+rHigh+' High</span><span style="color:#ff9800;">\u25CF '+rMed+' Medium</span><span style="color:#2196f3;">\u25CF '+rLow+' Low</span></div></div>';
  }

  el.innerHTML = html;
}

// === UX TAB ===
function renderUX() {
  if (!selectedProject) return;
  var el = document.getElementById('tc-ux');
  var ux = selectedProject.ux;
  if (!ux) { el.innerHTML = '<div class="empty-state">UX design data not yet available for this project.</div>'; return; }
  var html = '';

  // === UX Maturity Scorecard (KPIs) ===
  var personasVal = ux.personas.filter(function(p){return p.status==='validated'}).length;
  var journeysMapped = ux.journeys.filter(function(j){return j.status==='mapped'}).length;
  var fp = ux.userFlows.total>0?Math.round(ux.userFlows.mapped/ux.userFlows.total*100):0;
  var tp = ux.designSystem.tokens.total>0?Math.round(ux.designSystem.tokens.defined/ux.designSystem.tokens.total*100):0;
  var ap = ux.accessibility.criteria>0?Math.round(ux.accessibility.met/ux.accessibility.criteria*100):0;
  var overallUx = Math.round((fp + tp + ap) / 3);
  html += '<div class="mf-summary"><div class="mf-kpi"><span class="mf-kpi-val">' + overallUx + '%</span><span class="mf-kpi-lbl">UX Maturity</span></div><div class="mf-kpi"><span class="mf-kpi-val">' + personasVal + '/' + ux.personas.length + '</span><span class="mf-kpi-lbl">Personas</span></div><div class="mf-kpi"><span class="mf-kpi-val">' + journeysMapped + '/' + ux.journeys.length + '</span><span class="mf-kpi-lbl">Journeys</span></div><div class="mf-kpi"><span class="mf-kpi-val" style="color:' + (ap>=70?'#4caf50':'#ff9800') + ';">' + ap + '%</span><span class="mf-kpi-lbl">A11y</span></div></div>';


  // === Design Maturity Radar ===
  var wp = ux.wireframes?Math.round(ux.wireframes.approved/(ux.wireframes.total||1)*100):0;
  var cp = ux.designSystem.components.total>0?Math.round(ux.designSystem.components.specified/ux.designSystem.components.total*100):0;
  var pp = ux.personas.length>0?Math.round(personasVal/ux.personas.length*100):0;
  var jp = ux.journeys.length>0?Math.round(journeysMapped/ux.journeys.length*100):0;
  var axes = [{label:'Personas',val:pp},{label:'Journeys',val:jp},{label:'Flows',val:fp},{label:'Wireframes',val:wp},{label:'Tokens',val:tp},{label:'Components',val:cp},{label:'A11y',val:ap}];
  var cx=120, cy=110, maxR=80;
  html += '<div class="uxe-radar-card"><div class="pmx-timeline-title" style="margin-top:0;">Design Maturity Radar</div><svg viewBox="0 0 240 220" class="uxe-radar-svg">';
  [0.25,0.5,0.75,1].forEach(function(s) { html += '<circle cx="'+cx+'" cy="'+cy+'" r="'+(maxR*s)+'" fill="none" stroke="var(--border)" stroke-width="0.5" stroke-dasharray="2,2"/>'; });
  axes.forEach(function(a, i) {
    var angle = (Math.PI*2/axes.length)*i - Math.PI/2;
    var x2 = cx + Math.cos(angle)*maxR; var y2 = cy + Math.sin(angle)*maxR;
    var lx = cx + Math.cos(angle)*(maxR+14); var ly = cy + Math.sin(angle)*(maxR+14);
    html += '<line x1="'+cx+'" y1="'+cy+'" x2="'+x2+'" y2="'+y2+'" stroke="var(--border)" stroke-width="0.5"/>';
    html += '<text x="'+lx+'" y="'+ly+'" text-anchor="middle" font-size="7" fill="var(--text-secondary)">'+a.label+'</text>';
  });
  var points = axes.map(function(a, i) { var angle=(Math.PI*2/axes.length)*i-Math.PI/2; var r=maxR*(a.val/100); return (cx+Math.cos(angle)*r)+','+(cy+Math.sin(angle)*r); }).join(' ');
  html += '<polygon points="'+points+'" fill="#9c27b022" stroke="#9c27b0" stroke-width="1.5"/>';
  axes.forEach(function(a, i) { var angle=(Math.PI*2/axes.length)*i-Math.PI/2; var r=maxR*(a.val/100); html += '<circle cx="'+(cx+Math.cos(angle)*r)+'" cy="'+(cy+Math.sin(angle)*r)+'" r="3" fill="#9c27b0"/>'; });
  html += '</svg><div class="uxe-radar-legend">';
  axes.forEach(function(a) { var c = a.val>=70?'#4caf50':(a.val>=40?'#ff9800':'#f44336'); html += '<span class="uxe-radar-item"><span style="color:'+c+';font-weight:700;">'+a.val+'%</span> '+a.label+'</span>'; });
  html += '</div></div>';

  // === Journey Emotion Map ===
  var hasEmotionData = ux.journeys.filter(function(j){return j.stepDetails&&j.stepDetails.length}).length > 0;
  if (hasEmotionData) {
    html += '<div class="uxe-emotion-map"><div class="pmx-timeline-title" style="margin-top:0;border:none;padding:0;">Journey Emotion Map</div>';
    ux.journeys.forEach(function(j) {
      if (!j.stepDetails || !j.stepDetails.length) return;
      html += '<div class="uxe-emo-row"><span class="uxe-emo-label">' + j.name.split(' ').slice(0,2).join(' ') + '</span><div class="uxe-emo-cells">';
      j.stepDetails.forEach(function(s) { var color = s.emotion==='positive'?'#4caf50':(s.emotion==='frustrated'?'#f44336':'#616161'); html += '<div class="uxe-emo-cell" style="background:'+color+';" title="'+s.name+' ('+s.emotion+')"></div>'; });
      html += '</div></div>';
    });
    html += '<div class="uxe-emo-legend"><span>\uD83D\uDFE2 Positive</span><span>\uD83D\uDD34 Frustrated</span><span>\u26AB Neutral</span></div></div>';
  }

  // === Design System Health Rings ===
  html += '<div class="uxe-ds-health">';
  var dsItems = [{label:'Tokens',done:ux.designSystem.tokens.defined,total:ux.designSystem.tokens.total,color:'#9c27b0'},{label:'Components',done:ux.designSystem.components.specified,total:ux.designSystem.components.total,color:'#2196f3'}];
  if (ux.wireframes) dsItems.push({label:'Wireframes',done:ux.wireframes.approved,total:ux.wireframes.total,color:'#ff9800'});
  dsItems.push({label:'Accessibility',done:ux.accessibility.met,total:ux.accessibility.criteria,color:'#4caf50'});
  dsItems.forEach(function(d) { var pct=d.total>0?Math.round(d.done/d.total*100):0; html += '<div class="uxe-ds-item"><div class="uxe-ds-ring"><svg viewBox="0 0 40 40"><circle cx="20" cy="20" r="16" fill="none" stroke="var(--bg-hover)" stroke-width="4"/><circle cx="20" cy="20" r="16" fill="none" stroke="'+d.color+'" stroke-width="4" stroke-dasharray="'+(pct*1.005)+' 100.5" stroke-linecap="round" transform="rotate(-90 20 20)"/></svg><span class="uxe-ds-pct">'+pct+'%</span></div><span class="uxe-ds-label">'+d.label+'</span><span class="uxe-ds-count">'+d.done+'/'+d.total+'</span></div>'; });
  html += '</div>';

  // === Coverage Matrix ===
  html += '<div class="uxe-coverage"><table class="uxe-matrix"><thead><tr><th></th>';
  ux.personas.forEach(function(p){ html += '<th>'+p.name.split(' ')[0]+'</th>'; });
  html += '</tr></thead><tbody>';
  ux.journeys.forEach(function(j) {
    html += '<tr><td class="uxe-matrix-journey">'+j.name.split(' ').slice(0,2).join(' ')+'</td>';
    ux.personas.forEach(function(p) { var shortP = p.name.split(' \u2014 ')[0].split(' - ')[0]; var match = j.persona===shortP||j.persona===p.name; var color = match?(j.status==='mapped'?'#4caf50':'#ff9800'):'transparent'; html += '<td><div class="uxe-matrix-cell" style="background:'+color+';"></div></td>'; });
    html += '</tr>';
  });
  html += '</tbody></table></div>';

  // === Separator ===
  html += '<div style="border-top:1px solid var(--border);margin:16px 0;"></div>';

  // === Personas — collapsible, expandable ===
  var pVal = ux.personas.filter(function(p){return p.status==='validated'}).length;
  var pIp = ux.personas.length - pVal;
  html += '<div class="mf-group" id="ux-grp-personas"><div class="mf-group-hdr" onclick="document.getElementById(\'ux-grp-personas\').classList.toggle(\'collapsed\')" style="border-left-color:#9c27b0;"><span class="mf-grp-arrow">\u25BC</span><span class="mf-grp-icon">\uD83D\uDC64</span><span class="mf-grp-label">Personas</span><span class="mf-grp-status-pills"><span class="mf-grp-spill" style="color:#4caf50;">' + pVal + ' validated</span>' + (pIp>0?'<span class="mf-grp-spill" style="color:#ff9800;">' + pIp + ' in progress</span>':'') + '</span><span class="mf-grp-count">' + ux.personas.length + '</span></div><div class="mf-group-body">';
  ux.personas.forEach(function(p, pi) {
    var sc = p.status==='validated'?'#4caf50':'#ff9800';
    var relatedJourneys = ux.journeys.filter(function(j){return j.persona === p.name.split(' \u2014 ')[0] || j.persona === p.name;});
    html += '<div class="mf-item" id="ux-persona-' + pi + '"><div class="mf-item-hdr" onclick="toggleMfItem(\'ux-persona-' + pi + '\',event)"><span class="mf-item-dot" style="background:' + sc + ';"></span><span class="mf-item-title">' + p.name + '</span><span class="mf-item-status" style="color:' + sc + ';">' + p.status + '</span>' + (p.path ? '<a class="mf-item-link" href="#" onclick="openArtifact(\'' + (p.path||'').replace(/'/g, "\\'") + '\',event);return false;" title="' + (p.path||'') + '">\uD83D\uDCC4</a>' : '') + '</div>';
    html += '<div class="mf-item-body">';
    if (p.description) html += '<div class="mf-item-desc">' + p.description + '</div>';
    if (relatedJourneys.length > 0) {
      html += '<div class="po-stories" style="margin-top:6px;"><strong style="font-size:10px;color:var(--text-heading);">Related Journeys:</strong>';
      relatedJourneys.forEach(function(j) { var jc = j.status==='mapped'?'dot-produced':'dot-active'; html += '<div class="po-story-row"><span class="doc-dot ' + jc + '"></span><span style="flex:1;">' + j.name + '</span><span style="font-size:10px;color:var(--text-secondary);">' + j.steps + ' steps</span></div>'; });
      html += '</div>';
    }
    html += '</div></div>';
  });
  html += '</div></div>';

  // === User Journeys — collapsible, expandable ===
  html += '<div class="mf-group" id="ux-grp-journeys"><div class="mf-group-hdr" onclick="document.getElementById(\'ux-grp-journeys\').classList.toggle(\'collapsed\')" style="border-left-color:#2196f3;"><span class="mf-grp-arrow">\u25BC</span><span class="mf-grp-icon">\uD83D\uDDFA\uFE0F</span><span class="mf-grp-label">User Journeys</span><span class="mf-grp-status-pills"><span class="mf-grp-spill" style="color:#4caf50;">' + journeysMapped + ' mapped</span><span class="mf-grp-spill" style="color:#ff9800;">' + (ux.journeys.length - journeysMapped) + ' pending</span></span><span class="mf-grp-count">' + ux.journeys.length + '</span></div><div class="mf-group-body">';
  ux.journeys.forEach(function(j, ji) {
    var sc = j.status==='mapped'?'#4caf50':'#ff9800';
    html += '<div class="mf-item" id="ux-journey-' + ji + '"><div class="mf-item-hdr" onclick="toggleMfItem(\'ux-journey-' + ji + '\',event)"><span class="mf-item-dot" style="background:' + sc + ';"></span><span class="mf-item-title">' + j.name + '</span><span class="mf-item-status" style="color:' + sc + ';">' + j.persona + ' \u00B7 ' + (j.steps||0) + ' steps</span>' + (j.path ? '<a class="mf-item-link" href="#" onclick="openArtifact(\'' + (j.path||'').replace(/'/g, "\\'") + '\',event);return false;" title="' + (j.path||'') + '">\uD83D\uDCC4</a>' : '') + '</div>';
    html += '<div class="mf-item-body">';
    if (j.goal) html += '<div class="ux-journey-goal">\uD83C\uDFAF ' + j.goal + '</div>';
    if (j.trigger) html += '<div class="mf-item-meta"><span>\u26A1 Trigger: ' + j.trigger + '</span></div>';
    if (j.endStateSuccess) html += '<div class="mf-item-meta"><span>\u2705 Success: ' + j.endStateSuccess + '</span></div>';
    if (j.endStateFailure) html += '<div class="mf-item-meta"><span>\u274C Failure: ' + j.endStateFailure + '</span></div>';
    if (j.duration) html += '<div class="mf-item-meta"><span>\u23F1 Duration: ' + j.duration + '</span></div>';
    if (j.frequency) html += '<div class="mf-item-meta"><span>\uD83D\uDD01 Frequency: ' + j.frequency + '</span></div>';
    if (j.touchpoints && j.touchpoints.length) { html += '<div class="ux-journey-row"><span class="ux-journey-label">Touchpoints</span><span class="ux-journey-tags">'; j.touchpoints.forEach(function(t) { html += '<span class="ux-tag">' + t + '</span>'; }); html += '</span></div>'; }
    if (j.painPoints && j.painPoints.length) { html += '<div class="ux-journey-row"><span class="ux-journey-label" style="color:#f44336;">\u26A0 Pain Points</span><div class="ux-journey-list">'; j.painPoints.forEach(function(p) { html += '<div class="ux-pain">' + p + '</div>'; }); html += '</div></div>'; }
    if (j.opportunities && j.opportunities.length) { html += '<div class="ux-journey-row"><span class="ux-journey-label" style="color:#4caf50;">\u2728 Opportunities</span><div class="ux-journey-list">'; j.opportunities.forEach(function(o) { html += '<div class="ux-opp">' + o + '</div>'; }); html += '</div></div>'; }
    if (j.stepDetails && j.stepDetails.length) {
      html += '<div class="ux-journey-steps"><span class="ux-journey-label">Journey Flow</span><div class="ux-step-flow">';
      j.stepDetails.forEach(function(s, si) {
        var emo = s.emotion === 'positive' ? '\uD83D\uDE0A' : (s.emotion === 'frustrated' ? '\uD83D\uDE23' : '\uD83D\uDE10');
        var emoCls = 'ux-step-' + s.emotion;
        html += '<div class="ux-step ' + emoCls + '"><span class="ux-step-num">' + (si+1) + '</span><span class="ux-step-name">' + s.name + '</span><span class="ux-step-emo">' + emo + '</span></div>';
        if (si < j.stepDetails.length - 1) html += '<div class="ux-step-arrow">\u2192</div>';
      });
      html += '</div></div>';
    }
    html += '</div></div>';
  });
  html += '</div></div>';

  // === User Flows — collapsible, expandable (like Personas/Journeys) ===
  var flows = ux.flows || [];
  if (flows.length > 0) {
    var flowsMapped = flows.filter(function(f){return f.status==='mapped'||f.status==='produced'}).length;
    html += '<div class="mf-group" id="ux-grp-flows"><div class="mf-group-hdr" onclick="document.getElementById(\'ux-grp-flows\').classList.toggle(\'collapsed\')" style="border-left-color:#ff9800;"><span class="mf-grp-arrow">\u25BC</span><span class="mf-grp-icon">\uD83D\uDD00</span><span class="mf-grp-label">User Flows</span><span class="mf-grp-status-pills"><span class="mf-grp-spill" style="color:#4caf50;">' + flowsMapped + ' mapped</span></span><span class="mf-grp-count">' + flows.length + '</span></div><div class="mf-group-body">';
    flows.forEach(function(f, fi) {
      var sc = (f.status==='mapped'||f.status==='produced')?'#4caf50':'#ff9800';
      html += '<div class="mf-item" id="ux-flow-' + fi + '"><div class="mf-item-hdr" onclick="toggleMfItem(\'ux-flow-' + fi + '\',event)"><span class="mf-item-dot" style="background:' + sc + ';"></span><span class="mf-item-title">' + f.name + '</span><span class="mf-item-status" style="color:' + sc + ';">' + (f.status||'mapped') + '</span>' + (f.path ? '<a class="mf-item-link" href="#" onclick="openArtifact(\'' + (f.path||'').replace(/'/g, "\\'") + '\',event);return false;" title="' + (f.path||'') + '">\uD83D\uDCC4</a>' : '') + '</div>';
      html += '<div class="mf-item-body">';
      if (f.description) html += '<div class="mf-item-desc">' + f.description + '</div>';
      if (f.persona) html += '<div class="mf-item-meta"><span>\uD83D\uDC64 Persona: ' + f.persona + '</span></div>';
      if (f.journey) html += '<div class="mf-item-meta"><span>\uD83D\uDDFA\uFE0F Journey: ' + f.journey + '</span></div>';
      if (f.mermaid) {
        var mermaidId = 'ux-flow-mermaid-' + fi;
        html += '<div class="mf-group collapsed" id="' + mermaidId + '-grp" style="margin-top:8px;"><div class="mf-group-hdr" onclick="document.getElementById(\'' + mermaidId + '-grp\').classList.toggle(\'collapsed\');renderFlowMermaid(\'' + mermaidId + '\')" style="border-left-color:#569cd6;padding:4px 8px;"><span class="mf-grp-arrow">\u25BC</span><span class="mf-grp-icon">\uD83D\uDCC8</span><span class="mf-grp-label" style="font-size:11px;">Flow Diagram</span></div><div class="mf-group-body"><div id="' + mermaidId + '" class="arch-diagram-box" data-mermaid="' + encodeURIComponent(f.mermaid) + '" style="min-height:60px;padding:8px;"></div></div></div>';
      }
      html += '</div></div>';
    });
    html += '</div></div>';
  }

  // === Wireframes — collapsible, compact chips grouped by experience ===
  if (ux.wireframes && ux.wireframes.screens) {
    var wf = ux.wireframes;
    var expColors = {'Primary User':'#9c27b0','Admin User':'#2196f3','Setup':'#ff9800','Reviewer':'#f44336'};
    html += '<div class="mf-group" id="ux-grp-wireframes"><div class="mf-group-hdr" onclick="document.getElementById(\'ux-grp-wireframes\').classList.toggle(\'collapsed\')" style="border-left-color:#e91e63;"><span class="mf-grp-arrow">\u25BC</span><span class="mf-grp-icon">\uD83D\uDCF1</span><span class="mf-grp-label">Wireframes</span><span class="mf-grp-status-pills"><span class="mf-grp-spill" style="color:var(--text-secondary);">' + wf.total + ' screens \u00B7 ' + (wf.experiences||[]).length + ' experiences</span></span><span class="mf-grp-count">' + wf.total + '</span></div><div class="mf-group-body">';
    (wf.experiences||[]).forEach(function(exp) {
      var ec = expColors[exp.name.split(' ')[0]] || '#888';
      html += '<div style="margin-bottom:8px;"><span style="font-size:10px;font-weight:700;text-transform:uppercase;color:' + ec + ';">' + exp.name + ' (' + exp.screens + ' screens)</span></div>';
      html += '<div style="display:flex;flex-wrap:wrap;gap:5px;margin-bottom:10px;">';
      var expScreens = (wf.screens||[]).filter(function(s){return s.persona===exp.name.split(' ')[0] || s.persona===exp.name;});
      if (expScreens.length > 0) {
        expScreens.forEach(function(s) { html += '<span class="ux-ds-chip" title="' + s.id + ': ' + s.name + ' (' + s.template + ')"><span class="ux-ds-chip-dot" style="background:' + ec + ';"></span>' + s.id + ': ' + s.name + '</span>'; });
      } else {
        exp.templates.forEach(function(t) { html += '<span class="ux-ds-chip"><span class="ux-ds-chip-dot" style="background:' + ec + ';"></span>' + t + '</span>'; });
      }
      html += '</div>';
    });
    if (wf.path) html += '<div style="margin-top:4px;"><a href="#" onclick="openArtifact(\'' + wf.path.replace(/'/g, "\\'") + '\',event);return false;" style="font-size:11px;color:var(--accent);">\uD83D\uDCC4 Open Screen Inventory</a></div>';
    html += '</div></div>';
  }

  // === Design System — collapsible, compact ===
  if (ux.designSystemFiles && ux.designSystemFiles.length) {
    var dsf = ux.designSystemFiles;
    var dsProduced = dsf.filter(function(f){return f.status==='produced'}).length;
    html += '<div class="mf-group" id="ux-grp-designsys"><div class="mf-group-hdr" onclick="document.getElementById(\'ux-grp-designsys\').classList.toggle(\'collapsed\')" style="border-left-color:#9c27b0;"><span class="mf-grp-arrow">\u25BC</span><span class="mf-grp-icon">\uD83C\uDFA8</span><span class="mf-grp-label">Design System</span><span class="mf-grp-status-pills"><span class="mf-grp-spill" style="color:#4caf50;">' + dsProduced + '/' + dsf.length + ' produced</span></span><span class="mf-grp-count">' + dsf.length + '</span></div><div class="mf-group-body">';
    html += '<div style="display:flex;flex-wrap:wrap;gap:6px;">';
    dsf.forEach(function(f) {
      var sc = f.status==='produced'?'#4caf50':(f.status==='in-progress'?'#ff9800':'#616161');
      var link = f.path ? 'onclick="openArtifact(\'' + (f.path||'').replace(/'/g, "\\'") + '\',event);return false;" style="cursor:pointer;"' : '';
      html += '<a href="#" ' + link + ' class="ux-ds-chip" title="' + (f.description||f.name) + '"><span class="ux-ds-chip-dot" style="background:' + sc + ';"></span>' + f.name + '</a>';
    });
    html += '</div>';
    html += '</div></div>';
  }

  // === Component Library — collapsible, compact chips grouped by type ===
  if (ux.componentLibrary && ux.componentLibrary.components) {
    var cl = ux.componentLibrary;
    var typeColors = {Atom:'#569cd6', Molecule:'#ff9800', Organism:'#9c27b0'};
    html += '<div class="mf-group" id="ux-grp-components"><div class="mf-group-hdr" onclick="document.getElementById(\'ux-grp-components\').classList.toggle(\'collapsed\')" style="border-left-color:#2196f3;"><span class="mf-grp-arrow">\u25BC</span><span class="mf-grp-icon">\uD83E\uDDE9</span><span class="mf-grp-label">Component Library</span><span class="mf-grp-status-pills"><span class="mf-grp-spill" style="color:var(--text-secondary);">' + cl.atoms + ' atoms \u00B7 ' + cl.molecules + ' molecules \u00B7 ' + cl.organisms + ' organisms</span></span><span class="mf-grp-count">' + cl.total + '</span></div><div class="mf-group-body">';
    ['Atom','Molecule','Organism'].forEach(function(type) {
      var items = cl.components.filter(function(c){return c.type===type});
      if (items.length === 0) return;
      var tc = typeColors[type]||'#888';
      html += '<div style="margin-bottom:8px;"><span style="font-size:10px;font-weight:700;text-transform:uppercase;color:' + tc + ';">' + type + 's (' + items.length + ')</span></div>';
      html += '<div style="display:flex;flex-wrap:wrap;gap:5px;margin-bottom:10px;">';
      items.forEach(function(c) {
        html += '<span class="ux-ds-chip" title="' + c.id + ': ' + c.name + '"><span class="ux-ds-chip-dot" style="background:' + tc + ';"></span>' + c.name + '</span>';
      });
      html += '</div>';
    });
    if (cl.path) html += '<div style="margin-top:4px;"><a href="#" onclick="openArtifact(\'' + cl.path.replace(/'/g, "\\'") + '\',event);return false;" style="font-size:11px;color:var(--accent);">\uD83D\uDCC4 Open Component Inventory</a></div>';
    html += '</div></div>';
  }

  // === Accessibility — collapsible, starts collapsed ===
  var acc = ux.accessibility; var wc = (acc.baselineDefined)?'#4caf50':'#ff9800';
  html += '<div class="mf-group collapsed" id="ux-grp-a11y"><div class="mf-group-hdr" onclick="document.getElementById(\'ux-grp-a11y\').classList.toggle(\'collapsed\')" style="border-left-color:#4caf50;"><span class="mf-grp-arrow">\u25BC</span><span class="mf-grp-icon">\u267F</span><span class="mf-grp-label">Accessibility</span><span class="mf-grp-status-pills"><span class="mf-grp-spill" style="color:' + wc + ';">' + acc.target + ' ' + acc.wcagLevel + ' \u00B7 ' + ap + '% met</span></span><span class="mf-grp-count">' + acc.met + '/' + acc.criteria + '</span></div><div class="mf-group-body">';
  html += '<div style="padding:8px 0;"><div style="display:inline-flex;align-items:center;gap:6px;padding:4px 10px;border-radius:6px;background:' + wc + '22;border:1px solid ' + wc + '44;color:' + wc + ';font-size:12px;font-weight:600;margin-bottom:8px;">\u267F ' + (acc.target||'WCAG') + ' Level ' + (acc.wcagLevel||'AA') + ((acc.baselineDefined)?' \u2713':' pending') + '</div>';
  html += '<div style="display:flex;justify-content:space-between;font-size:12px;margin-bottom:4px;"><span>Criteria Met</span><span>' + acc.met + '/' + acc.criteria + ' (' + ap + '%)</span></div><div class="progress-bar"><div class="progress-fill ' + (ap>=70?'complete':'active') + '" style="width:' + ap + '%"></div></div></div>';
  html += '</div></div>';

  // === Research Insights — collapsible, starts collapsed, sorted by impact ===
  if (ux.researchInsights && ux.researchInsights.length) {
    var hiCount = ux.researchInsights.filter(function(r){return r.impact==='High'}).length;
    var mdCount = ux.researchInsights.filter(function(r){return r.impact==='Medium'}).length;
    html += '<div class="mf-group collapsed" id="ux-grp-insights"><div class="mf-group-hdr" onclick="document.getElementById(\'ux-grp-insights\').classList.toggle(\'collapsed\')" style="border-left-color:#e91e63;"><span class="mf-grp-arrow">\u25BC</span><span class="mf-grp-icon">\uD83D\uDD2C</span><span class="mf-grp-label">Research Insights</span><span class="mf-grp-status-pills"><span class="mf-grp-spill" style="color:#f44336;">' + hiCount + ' high</span><span class="mf-grp-spill" style="color:#ff9800;">' + mdCount + ' medium</span></span><span class="mf-grp-count">' + ux.researchInsights.length + '</span></div><div class="mf-group-body">';
    var sorted = ux.researchInsights.slice().sort(function(a,b) { var o = {High:0,Medium:1,Low:2}; return (o[a.impact]||3) - (o[b.impact]||3); });
    sorted.forEach(function(r) {
      var ic = r.impact==='High'?'#f44336':(r.impact==='Medium'?'#ff9800':'#2196f3');
      html += '<div class="mf-item"><div class="mf-item-hdr" style="cursor:default;align-items:flex-start;"><span class="mf-item-dot" style="background:' + ic + ';margin-top:4px;"></span><span class="mf-item-title" style="white-space:normal;line-height:1.4;">' + r.finding + '</span><span class="mf-item-status" style="color:' + ic + ';">' + r.impact + '</span></div><div style="padding:0 0 2px 21px;font-size:10px;color:var(--text-secondary);">Source: ' + r.source + '</div></div>';
    });
    html += '</div></div>';
  }

  el.innerHTML = html;
  // Render persona-journey diagram
  setTimeout(function() { renderUXDiagram(ux); }, 50);
}

function renderUXDiagram(ux) {
  if (typeof mermaid === 'undefined') return;
  var theme = document.documentElement.getAttribute('data-theme') === 'light' ? 'default' : 'dark';
  mermaid.initialize({startOnLoad:false, theme:theme, flowchart:{useMaxWidth:true, curve:'basis'}, securityLevel:'loose'});

  var pjEl = document.getElementById('ux-mermaid-pj');
  if (!pjEl) return;

  var lines = ['graph LR'];
  // Create persona nodes
  var personaIds = {};
  ux.personas.forEach(function(p, i) {
    var id = 'P' + i;
    var shortName = p.name.split(' \u2014 ')[0].split(' - ')[0];
    personaIds[p.name] = id;
    personaIds[shortName] = id;
    var sc = p.status==='validated'?'#4caf50':'#ff9800';
    lines.push('  ' + id + '(("' + shortName.replace(/"/g,"'") + '"))');
    lines.push('  style ' + id + ' fill:' + sc + '22,stroke:' + sc + ',stroke-width:2px');
  });
  // Create journey nodes and connect
  ux.journeys.forEach(function(j, i) {
    var jId = 'J' + i;
    var sc = j.status==='mapped'?'#4caf50':'#ff9800';
    lines.push('  ' + jId + '["' + j.name.replace(/"/g,"'") + '"]');
    lines.push('  style ' + jId + ' fill:' + sc + '11,stroke:' + sc);
    // Connect persona to journey
    var pId = personaIds[j.persona];
    if (pId) {
      lines.push('  ' + pId + ' --> ' + jId);
    }
  });

  pjEl.removeAttribute('data-processed');
  pjEl.innerHTML = '<div class="mermaid">' + lines.join('\n') + '</div>';
  try { mermaid.init(undefined, pjEl.querySelector('.mermaid')); } catch(e) {}
}

// === Flow Mermaid Renderer (lazy — renders on expand) ===
function renderFlowMermaid(containerId) {
  if (typeof mermaid === 'undefined') return;
  var el = document.getElementById(containerId);
  if (!el || el.getAttribute('data-rendered')) return;
  var encoded = el.getAttribute('data-mermaid');
  if (!encoded) return;
  var code = decodeURIComponent(encoded);
  var theme = document.documentElement.getAttribute('data-theme') === 'light' ? 'default' : 'dark';
  mermaid.initialize({startOnLoad:false, theme:theme, flowchart:{useMaxWidth:true, curve:'basis'}, securityLevel:'loose'});
  el.style.position = 'relative';
  var ctrls = '<div class="arch-zoom-controls"><button class="arch-zoom-btn" onclick="archZoom(\'' + containerId + '\',1,event)" title="Zoom in">+</button><button class="arch-zoom-btn" onclick="archZoom(\'' + containerId + '\',-1,event)" title="Zoom out">\u2212</button><button class="arch-zoom-btn" onclick="archZoom(\'' + containerId + '\',0,event)" title="Reset">\u21BA</button><button class="arch-zoom-btn" onclick="archFullscreen(\'' + containerId + '\',event)" title="Fullscreen">\u26F6</button></div>';
  el.innerHTML = ctrls + '<div class="mermaid">' + code + '</div>';
  try { mermaid.init(undefined, el.querySelector('.mermaid')); } catch(e) { el.innerHTML = ctrls + '<pre style="font-size:10px;color:var(--text-secondary);overflow-x:auto;">' + code + '</pre>'; }
  el.setAttribute('data-rendered', 'true');
  archEnableMouse(containerId);
}

// === Diagram Fullscreen (overlay with zoom) ===
var archFsZoomLevel = 1;
function archFullscreen(boxId, evt) {
  if (evt) evt.stopPropagation();
  var box = document.getElementById(boxId);
  if (!box) return;
  var code = decodeURIComponent(box.getAttribute('data-mermaid') || '');
  if (!code) return;
  var overlay = document.getElementById('arch-fs-overlay');
  if (!overlay) {
    overlay = document.createElement('div');
    overlay.id = 'arch-fs-overlay';
    overlay.className = 'arch-fs-overlay';
    document.body.appendChild(overlay);
  }
  overlay.innerHTML = '<div class="arch-fs-bar"><button class="arch-zoom-btn" onclick="archZoom(\'arch-fs-body\',1,event)" title="Zoom in">+</button><button class="arch-zoom-btn" onclick="archZoom(\'arch-fs-body\',-1,event)" title="Zoom out">\u2212</button><button class="arch-zoom-btn" onclick="archZoom(\'arch-fs-body\',0,event)" title="Reset">\u21BA</button><button class="arch-zoom-btn" onclick="closeArchFs()" title="Close">\u2715</button></div><div class="arch-fs-body" id="arch-fs-body"><div class="mermaid">' + code + '</div></div>';
  overlay.style.display = 'flex';
  archTf['arch-fs-body'] = {s:1, x:0, y:0};
  var theme = document.documentElement.getAttribute('data-theme') === 'light' ? 'default' : 'dark';
  try { mermaid.initialize({startOnLoad:false, theme:theme, securityLevel:'loose'}); mermaid.init(undefined, overlay.querySelector('.mermaid')); archEnableMouse('arch-fs-body'); } catch(e) {}
}
function archFsZoom(dir) {
  var b = document.getElementById('arch-fs-body');
  if (!b) return;
  var m = b.querySelector('.mermaid');
  if (!m) return;
  if (dir === 0) archFsZoomLevel = 1; else archFsZoomLevel = Math.max(0.5, Math.min(5, archFsZoomLevel + dir * 0.25));
  m.style.transformOrigin = 'top left';
  m.style.transform = 'scale(' + archFsZoomLevel + ')';
}
function closeArchFs() {
  var o = document.getElementById('arch-fs-overlay');
  if (o) o.style.display = 'none';
}

// === UX-EXT TAB (UX Designer visual cockpit) ===
function renderUXExt() {
  if (!selectedProject) return;
  var el = document.getElementById('tc-ux-ext');
  var ux = selectedProject.ux;
  if (!ux) { el.innerHTML = '<div class="empty-state">UX design data not yet available.</div>'; return; }
  var html = '';

  // === Design Maturity Radar (SVG) ===
  var fp = ux.userFlows.total>0?Math.round(ux.userFlows.mapped/ux.userFlows.total*100):0;
  var tp = ux.designSystem.tokens.total>0?Math.round(ux.designSystem.tokens.defined/ux.designSystem.tokens.total*100):0;
  var cp = ux.designSystem.components.total>0?Math.round(ux.designSystem.components.specified/ux.designSystem.components.total*100):0;
  var ap = ux.accessibility.criteria>0?Math.round(ux.accessibility.met/ux.accessibility.criteria*100):0;
  var wp = ux.wireframes?Math.round(ux.wireframes.approved/(ux.wireframes.total||1)*100):0;
  var pp = ux.personas.length>0?Math.round(ux.personas.filter(function(p){return p.status==='validated'}).length/ux.personas.length*100):0;
  var jp = ux.journeys.length>0?Math.round(ux.journeys.filter(function(j){return j.status==='mapped'}).length/ux.journeys.length*100):0;

  // Radar chart points (7 axes)
  var axes = [{label:'Personas',val:pp},{label:'Journeys',val:jp},{label:'Flows',val:fp},{label:'Wireframes',val:wp},{label:'Tokens',val:tp},{label:'Components',val:cp},{label:'A11y',val:ap}];
  var cx=120, cy=110, maxR=80;
  html += '<div class="uxe-radar-card"><div class="pmx-timeline-title">Design Maturity Radar</div><svg viewBox="0 0 240 220" class="uxe-radar-svg">';
  // Grid circles
  [0.25,0.5,0.75,1].forEach(function(s) { html += '<circle cx="'+cx+'" cy="'+cy+'" r="'+(maxR*s)+'" fill="none" stroke="var(--border)" stroke-width="0.5" stroke-dasharray="2,2"/>'; });
  // Axis lines + labels
  axes.forEach(function(a, i) {
    var angle = (Math.PI*2/axes.length)*i - Math.PI/2;
    var x2 = cx + Math.cos(angle)*maxR;
    var y2 = cy + Math.sin(angle)*maxR;
    var lx = cx + Math.cos(angle)*(maxR+14);
    var ly = cy + Math.sin(angle)*(maxR+14);
    html += '<line x1="'+cx+'" y1="'+cy+'" x2="'+x2+'" y2="'+y2+'" stroke="var(--border)" stroke-width="0.5"/>';
    html += '<text x="'+lx+'" y="'+ly+'" text-anchor="middle" font-size="7" fill="var(--text-secondary)">'+a.label+'</text>';
  });
  // Data polygon
  var points = axes.map(function(a, i) {
    var angle = (Math.PI*2/axes.length)*i - Math.PI/2;
    var r = maxR * (a.val/100);
    return (cx + Math.cos(angle)*r) + ',' + (cy + Math.sin(angle)*r);
  }).join(' ');
  html += '<polygon points="'+points+'" fill="#9c27b022" stroke="#9c27b0" stroke-width="1.5"/>';
  // Data points
  axes.forEach(function(a, i) {
    var angle = (Math.PI*2/axes.length)*i - Math.PI/2;
    var r = maxR * (a.val/100);
    var px = cx + Math.cos(angle)*r;
    var py = cy + Math.sin(angle)*r;
    html += '<circle cx="'+px+'" cy="'+py+'" r="3" fill="#9c27b0"/>';
  });
  html += '</svg><div class="uxe-radar-legend">';
  axes.forEach(function(a) { var c = a.val>=70?'#4caf50':(a.val>=40?'#ff9800':'#f44336'); html += '<span class="uxe-radar-item"><span style="color:'+c+';font-weight:700;">'+a.val+'%</span> '+a.label+'</span>'; });
  html += '</div></div>';

  // === Emotion Journey Heatmap ===
  html += '<div class="pmx-timeline-title">Journey Emotion Map</div>';
  html += '<div class="uxe-emotion-map">';
  ux.journeys.forEach(function(j) {
    if (!j.stepDetails || !j.stepDetails.length) return;
    html += '<div class="uxe-emo-row"><span class="uxe-emo-label">' + j.name.split(' ').slice(0,2).join(' ') + '</span><div class="uxe-emo-cells">';
    j.stepDetails.forEach(function(s) {
      var color = s.emotion==='positive'?'#4caf50':(s.emotion==='frustrated'?'#f44336':'#616161');
      html += '<div class="uxe-emo-cell" style="background:'+color+';" title="'+s.name+' ('+s.emotion+')"></div>';
    });
    html += '</div></div>';
  });
  if (ux.journeys.filter(function(j){return j.stepDetails&&j.stepDetails.length}).length === 0) {
    html += '<div style="font-size:11px;color:var(--text-secondary);padding:8px;">No step-level emotion data available yet.</div>';
  }
  html += '<div class="uxe-emo-legend"><span>\uD83D\uDFE2 Positive</span><span>\uD83D\uDD34 Frustrated</span><span>\u26AB Neutral</span></div></div>';

  // === Design System Health ===
  html += '<div class="pmx-timeline-title">Design System Health</div>';
  html += '<div class="uxe-ds-health">';
  var dsItems = [
    {label:'Tokens',done:ux.designSystem.tokens.defined,total:ux.designSystem.tokens.total,color:'#9c27b0'},
    {label:'Components',done:ux.designSystem.components.specified,total:ux.designSystem.components.total,color:'#2196f3'}
  ];
  if (ux.wireframes) dsItems.push({label:'Wireframes',done:ux.wireframes.approved,total:ux.wireframes.total,color:'#ff9800'});
  dsItems.push({label:'Accessibility',done:ux.accessibility.met,total:ux.accessibility.criteria,color:'#4caf50'});
  dsItems.forEach(function(d) {
    var pct = d.total>0?Math.round(d.done/d.total*100):0;
    html += '<div class="uxe-ds-item"><div class="uxe-ds-ring"><svg viewBox="0 0 40 40"><circle cx="20" cy="20" r="16" fill="none" stroke="var(--bg-hover)" stroke-width="4"/><circle cx="20" cy="20" r="16" fill="none" stroke="'+d.color+'" stroke-width="4" stroke-dasharray="'+(pct*1.005)+' 100.5" stroke-linecap="round" transform="rotate(-90 20 20)"/></svg><span class="uxe-ds-pct">'+pct+'%</span></div><span class="uxe-ds-label">'+d.label+'</span><span class="uxe-ds-count">'+d.done+'/'+d.total+'</span></div>';
  });
  html += '</div>';

  // === Research Impact Summary ===
  if (ux.researchInsights && ux.researchInsights.length) {
    var hi = ux.researchInsights.filter(function(r){return r.impact==='High'}).length;
    var md = ux.researchInsights.filter(function(r){return r.impact==='Medium'}).length;
    var lo = ux.researchInsights.filter(function(r){return r.impact==='Low'}).length;
    html += '<div class="pmx-timeline-title">Research Impact</div>';
    html += '<div class="uxe-research-summary"><div class="uxe-impact-bar">';
    var total = ux.researchInsights.length;
    if (hi) html += '<div class="uxe-impact-seg" style="width:'+(hi/total*100)+'%;background:#f44336;" title="'+hi+' High Impact"></div>';
    if (md) html += '<div class="uxe-impact-seg" style="width:'+(md/total*100)+'%;background:#ff9800;" title="'+md+' Medium Impact"></div>';
    if (lo) html += '<div class="uxe-impact-seg" style="width:'+(lo/total*100)+'%;background:#2196f3;" title="'+lo+' Low Impact"></div>';
    html += '</div><div class="uxe-impact-labels"><span style="color:#f44336;">\u25CF '+hi+' High</span><span style="color:#ff9800;">\u25CF '+md+' Medium</span><span style="color:#2196f3;">\u25CF '+lo+' Low</span><span style="color:var(--text-secondary);">'+total+' total</span></div></div>';
  }

  // === Coverage Matrix (Persona x Journey) ===
  html += '<div class="pmx-timeline-title">Coverage Matrix</div>';
  html += '<div class="uxe-coverage"><table class="uxe-matrix"><thead><tr><th></th>';
  var personaShort = ux.personas.map(function(p){ return p.name.split(' ')[0]; });
  personaShort.forEach(function(n){ html += '<th>'+n+'</th>'; });
  html += '</tr></thead><tbody>';
  ux.journeys.forEach(function(j) {
    html += '<tr><td class="uxe-matrix-journey">'+j.name.split(' ').slice(0,2).join(' ')+'</td>';
    ux.personas.forEach(function(p) {
      var shortP = p.name.split(' \u2014 ')[0].split(' - ')[0];
      var match = j.persona === shortP || j.persona === p.name;
      var color = match ? (j.status==='mapped'?'#4caf50':'#ff9800') : 'transparent';
      html += '<td><div class="uxe-matrix-cell" style="background:'+color+';"></div></td>';
    });
    html += '</tr>';
  });
  html += '</tbody></table></div>';

  el.innerHTML = html;
}

// === MGMT TAB (MF) ===
function renderMgmt() {
  if (!selectedProject) return;
  var el = document.getElementById('tc-mgmt');
  var detail = (selectedProject.mgmtDetail) || {};
  if (!detail || (!detail.decisions && !detail.risks)) { el.innerHTML = '<div class="empty-state">Management framework data not available.</div>'; return; }

  var mgmtIcons = {decisions:'\uD83D\uDCCB',risks:'\u26A0\uFE0F',changes:'\uD83D\uDD04',actions:'\u2705',issues:'\uD83D\uDC1B',lessons:'\uD83D\uDCA1'};
  var mgmtColors = {decisions:'#569cd6',risks:'#f44336',changes:'#ff9800',actions:'#4caf50',issues:'#e91e63',lessons:'#9c27b0'};
  var statusDots = {
    // Green: Done — no further action needed
    Approved:'#4caf50', Complete:'#4caf50', Resolved:'#4caf50', Captured:'#4caf50', Closed:'#4caf50',
    // Blue: Active — work in progress
    'In Progress':'#2196f3', Mitigating:'#2196f3', Investigating:'#2196f3', 'In Review':'#2196f3',
    // Orange: Attention — open/waiting/needs decision
    Open:'#ff9800', Pending:'#ff9800', Proposed:'#ff9800',
    // Red: Critical — blocked or rejected
    Blocked:'#f44336', Rejected:'#f44336'
  };
  var registers = ['decisions','risks','changes','actions','issues','lessons'];

  // Summary KPIs
  var totalItems = 0; registers.forEach(function(k) { totalItems += (detail[k]||[]).length; });
  var openItems = 0; registers.forEach(function(k) { (detail[k]||[]).forEach(function(i) { var s = (i.status||'').toLowerCase(); if (s === 'open' || s === 'in progress' || s === 'investigating' || s === 'pending' || s === 'proposed' || s === 'in review' || s === 'mitigating') openItems++; }); });
  var closedItems = totalItems - openItems;

  var html = '<div class="mf-summary"><div class="mf-kpi"><span class="mf-kpi-val">' + totalItems + '</span><span class="mf-kpi-lbl">Total</span></div><div class="mf-kpi"><span class="mf-kpi-val" style="color:#ff9800;">' + openItems + '</span><span class="mf-kpi-lbl">Open</span></div><div class="mf-kpi"><span class="mf-kpi-val" style="color:#4caf50;">' + closedItems + '</span><span class="mf-kpi-lbl">Closed</span></div></div>';

  // === Resolution Flow (funnel: open → active → closed) ===
  var activeItems = 0; registers.forEach(function(k) { (detail[k]||[]).forEach(function(i) { var s = (i.status||'').toLowerCase(); if (s === 'in progress' || s === 'mitigating' || s === 'investigating' || s === 'in review') activeItems++; }); });
  var pureOpen = openItems - activeItems;
  var maxFunnel = Math.max(pureOpen, activeItems, closedItems, 1);
  html += '<div class="mf-flow-card"><div class="pmx-timeline-title" style="margin-top:0;">Resolution Flow</div><div class="mf-funnel">';
  html += '<div class="mf-funnel-stage"><div class="mf-funnel-bar" style="width:' + (pureOpen/maxFunnel*100) + '%;background:#ff9800;"></div><span class="mf-funnel-label">\u26A0 Awaiting (' + pureOpen + ')</span></div>';
  html += '<div class="mf-funnel-arrow">\u25BC</div>';
  html += '<div class="mf-funnel-stage"><div class="mf-funnel-bar" style="width:' + (activeItems/maxFunnel*100) + '%;background:#2196f3;"></div><span class="mf-funnel-label">\u26A1 In Progress (' + activeItems + ')</span></div>';
  html += '<div class="mf-funnel-arrow">\u25BC</div>';
  html += '<div class="mf-funnel-stage"><div class="mf-funnel-bar" style="width:' + (closedItems/maxFunnel*100) + '%;background:#4caf50;"></div><span class="mf-funnel-label">\u2705 Resolved (' + closedItems + ')</span></div>';
  html += '</div></div>';

  // === Register Heatmap (which registers have open items) ===
  html += '<div class="pmx-timeline-title">Register Pressure</div><div class="mf-register-heat">';
  registers.forEach(function(k) {
    var items = detail[k]||[];
    var regOpen = items.filter(function(i){ var s=(i.status||'').toLowerCase(); return s==='open'||s==='in progress'||s==='pending'||s==='proposed'||s==='investigating'||s==='mitigating'||s==='in review'; }).length;
    var regClosed = items.length - regOpen;
    var heat = items.length > 0 ? regOpen / items.length : 0;
    var heatColor = heat > 0.6 ? '#f44336' : (heat > 0.3 ? '#ff9800' : (heat > 0 ? '#2196f3' : '#4caf50'));
    var icon = mgmtIcons[k];
    html += '<div class="mf-heat-cell" style="border-color:' + heatColor + ';"><div class="mf-heat-icon">' + icon + '</div><div class="mf-heat-info"><span class="mf-heat-name">' + k.charAt(0).toUpperCase()+k.slice(1) + '</span><span class="mf-heat-counts"><span style="color:#ff9800;">' + regOpen + '</span>/<span style="color:#4caf50;">' + regClosed + '</span></span></div><div class="mf-heat-indicator" style="background:' + heatColor + ';width:' + Math.max(10, heat*100) + '%;"></div></div>';
  });
  html += '</div>';

  // === Governance Radar (SVG) ===
  var regAxes = registers.map(function(k) { var items = detail[k]||[]; var resolved = items.filter(function(i){ var s=(i.status||'').toLowerCase(); return s==='approved'||s==='complete'||s==='resolved'||s==='captured'||s==='closed'; }).length; return {label:k.charAt(0).toUpperCase()+k.slice(1,4), val: items.length>0?Math.round(resolved/items.length*100):100}; });
  var gcx=120, gcy=100, gmaxR=70;
  html += '<div class="uxe-radar-card"><div class="pmx-timeline-title" style="margin-top:0;">Governance Health Radar</div><svg viewBox="0 0 240 200" class="uxe-radar-svg">';
  [0.5,1].forEach(function(s) { html += '<circle cx="'+gcx+'" cy="'+gcy+'" r="'+(gmaxR*s)+'" fill="none" stroke="var(--border)" stroke-width="0.5" stroke-dasharray="2,2"/>'; });
  regAxes.forEach(function(a, i) { var angle=(Math.PI*2/regAxes.length)*i-Math.PI/2; var x2=gcx+Math.cos(angle)*gmaxR; var y2=gcy+Math.sin(angle)*gmaxR; var lx=gcx+Math.cos(angle)*(gmaxR+14); var ly=gcy+Math.sin(angle)*(gmaxR+14); html += '<line x1="'+gcx+'" y1="'+gcy+'" x2="'+x2+'" y2="'+y2+'" stroke="var(--border)" stroke-width="0.5"/>'; html += '<text x="'+lx+'" y="'+ly+'" text-anchor="middle" font-size="7" fill="var(--text-secondary)">'+a.label+'</text>'; });
  var gPoints = regAxes.map(function(a, i) { var angle=(Math.PI*2/regAxes.length)*i-Math.PI/2; var r=gmaxR*(a.val/100); return (gcx+Math.cos(angle)*r)+','+(gcy+Math.sin(angle)*r); }).join(' ');
  html += '<polygon points="'+gPoints+'" fill="#4caf5022" stroke="#4caf50" stroke-width="1.5"/>';
  regAxes.forEach(function(a, i) { var angle=(Math.PI*2/regAxes.length)*i-Math.PI/2; var r=gmaxR*(a.val/100); var c=a.val>=70?'#4caf50':(a.val>=40?'#ff9800':'#f44336'); html += '<circle cx="'+(gcx+Math.cos(angle)*r)+'" cy="'+(gcy+Math.sin(angle)*r)+'" r="3" fill="'+c+'"/>'; });
  html += '</svg><div class="uxe-radar-legend">';
  regAxes.forEach(function(a) { var c=a.val>=70?'#4caf50':(a.val>=40?'#ff9800':'#f44336'); html += '<span class="uxe-radar-item"><span style="color:'+c+';font-weight:700;">'+a.val+'%</span> resolved</span>'; });
  html += '</div></div>';

  // === Separator ===
  html += '<div style="border-top:1px solid var(--border);margin:16px 0;"></div>';

  registers.forEach(function(key) {
    var items = detail[key] || [];
    var icon = mgmtIcons[key]; var color = mgmtColors[key];
    var title = key.charAt(0).toUpperCase() + key.slice(1);

    // Count by status
    var statusCounts = {}; items.forEach(function(i) { var s = i.status||'Unknown'; statusCounts[s] = (statusCounts[s]||0)+1; });

    html += '<div class="mf-group collapsed" id="mf-grp-' + key + '">';
    // Build mini status summary for header — ordered by severity: red > orange > blue > green
    var statusSummaryHtml = '';
    var summaryOrder = ['Blocked','Rejected','Open','Pending','Proposed','In Progress','Mitigating','Investigating','In Review','Approved','Complete','Resolved','Captured','Closed'];
    var orderedKeys = summaryOrder.filter(function(s) { return statusCounts[s]; });
    if (orderedKeys.length > 0) {
      statusSummaryHtml = '<span class="mf-grp-status-pills">';
      orderedKeys.forEach(function(s) { var dc = statusDots[s] || '#888'; statusSummaryHtml += '<span class="mf-grp-spill" style="color:' + dc + ';">' + statusCounts[s] + ' ' + s + '</span>'; });
      statusSummaryHtml += '</span>';
    }
    html += '<div class="mf-group-hdr" onclick="toggleMfGroup(\'' + key + '\')" style="border-left-color:' + color + ';"><span class="mf-grp-arrow">\u25BC</span><span class="mf-grp-icon">' + icon + '</span><span class="mf-grp-label">' + title + '</span>' + statusSummaryHtml + '<span class="mf-grp-count">' + items.length + '</span></div>';
    html += '<div class="mf-group-body">';

    if (items.length === 0) {
      html += '<div class="empty-state" style="padding:10px;font-size:11px;">No ' + title.toLowerCase() + ' recorded</div>';
    } else {
      // Filter pills
      var statuses = Object.keys(statusCounts);
      if (statuses.length > 1) {
        html += '<div class="mf-filters"><span class="mf-pill active" onclick="mfFilter(\'' + key + '\',\'all\',event)">All ' + items.length + '</span>';
        statuses.forEach(function(s) { var dc = statusDots[s] || '#888'; html += '<span class="mf-pill" onclick="mfFilter(\'' + key + '\',\'' + s + '\',event)"><span class="mf-pill-dot" style="background:' + dc + ';"></span>' + s + ' ' + statusCounts[s] + '</span>'; });
        html += '</div>';
      }
      // Items
      items.forEach(function(item, idx) {
        var dotColor = statusDots[item.status] || '#888';
        var itemId = 'mf-item-' + key + '-' + idx;
        var fileLink = item.path ? '<a class="mf-item-link" href="#" onclick="openArtifact(\'' + (item.path||'').replace(/'/g, "\\'") + '\',event);return false;" title="' + (item.path||'') + '">\uD83D\uDCC4</a>' : '';
        html += '<div class="mf-item" id="' + itemId + '" data-status="' + (item.status||'') + '">';
        html += '<div class="mf-item-hdr" onclick="toggleMfItem(\'' + itemId + '\',event)"><span class="mf-item-dot" style="background:' + dotColor + ';"></span><span class="mf-item-id">' + (item.id||'') + '</span><span class="mf-item-title">' + (item.title||item.text||'') + '</span><span class="mf-item-status" style="color:' + dotColor + ';">' + (item.status||'') + '</span>' + fileLink + '</div>';
        html += '<div class="mf-item-body">';
        if (item.owner) html += '<div class="mf-item-meta"><span>Owner: ' + item.owner + '</span></div>';
        if (item.dueDate) html += '<div class="mf-item-meta"><span>Due: ' + item.dueDate + '</span></div>';
        if (item.description) html += '<div class="mf-item-desc">' + item.description + '</div>';
        if (item.path) html += '<div class="mf-item-file"><a href="#" onclick="openArtifact(\'' + (item.path||'').replace(/'/g, "\\'") + '\',event);return false;">\uD83D\uDCC4 ' + item.path + '</a></div>';
        html += '</div></div>';
      });
    }
    html += '</div></div>';
  });
  el.innerHTML = html;
}
function toggleMfGroup(key) { document.getElementById('mf-grp-' + key).classList.toggle('collapsed'); }
function toggleMfItem(id, evt) { if (evt) evt.stopPropagation(); var el = document.getElementById(id); if (el) el.classList.toggle('expanded'); }
function mfFilter(key, val, event) {
  event.stopPropagation();
  var grp = document.getElementById('mf-grp-' + key);
  grp.querySelectorAll('.mf-pill').forEach(function(p) { p.classList.remove('active'); });
  event.target.closest('.mf-pill').classList.add('active');
  grp.querySelectorAll('.mf-item').forEach(function(row) { row.style.display = (val === 'all' || row.getAttribute('data-status') === val) ? '' : 'none'; });
}

// === STATS RIGHT ===
function renderStatsRight() {
  if (!selectedProject) return;
  var el = document.getElementById('tc-stats-right');
  var p = selectedProject;
  var html = '';

  // Project health ring
  var totalArts = 0, doneArts = 0, blockerCount = 0, completePkgs = 0;
  p.packages.forEach(function(pkg) { totalArts += pkg.progress.total; doneArts += pkg.progress.done; blockerCount += pkg.blockers.length; if (pkg.status === 'complete') completePkgs++; });
  var artPct = totalArts > 0 ? Math.round(doneArts/totalArts*100) : 0;

  html += '<div class="pmx-hero" style="margin-bottom:14px;">';
  html += '<div class="pmx-ring-wrap"><svg class="pmx-ring" viewBox="0 0 100 100"><circle cx="50" cy="50" r="42" fill="none" stroke="var(--bg-hover)" stroke-width="8"/><circle cx="50" cy="50" r="42" fill="none" stroke="' + (p.status==='blocked'?'#f44336':'#4caf50') + '" stroke-width="8" stroke-dasharray="' + (p.progress * 2.64) + ' 264" stroke-linecap="round" transform="rotate(-90 50 50)"/><text x="50" y="46" text-anchor="middle" font-size="18" font-weight="700" fill="var(--text-heading)">' + p.progress + '%</text><text x="50" y="60" text-anchor="middle" font-size="7" fill="var(--text-secondary)">PROJECT</text></svg></div>';
  html += '<div class="pmx-hero-stats"><div class="pmx-stat"><span class="pmx-stat-val" style="color:#4caf50;">' + completePkgs + '/' + p.packages.length + '</span><span class="pmx-stat-lbl">Packages</span></div><div class="pmx-stat"><span class="pmx-stat-val">' + doneArts + '</span><span class="pmx-stat-lbl">Artifacts</span></div><div class="pmx-stat"><span class="pmx-stat-val" style="color:' + (blockerCount>0?'#f44336':'#4caf50') + ';">' + blockerCount + '</span><span class="pmx-stat-lbl">Blockers</span></div></div>';
  html += '</div>';

  // Package rings grid
  html += '<div class="stats-section-title">Package Progress</div>';
  html += '<div class="stats-project-grid">';
  p.packages.forEach(function(pkg) {
    var c = pkg.status==='complete'?'#4caf50':(pkg.status==='blocked'?'#f44336':(pkg.status==='active'?'#ff9800':'#616161'));
    html += '<div class="stats-proj-card"><svg viewBox="0 0 44 44" class="stats-mini-ring"><circle cx="22" cy="22" r="18" fill="none" stroke="var(--bg-hover)" stroke-width="4"/><circle cx="22" cy="22" r="18" fill="none" stroke="'+c+'" stroke-width="4" stroke-dasharray="'+(pkg.progress.pct*1.13)+' 113" stroke-linecap="round" transform="rotate(-90 22 22)"/><text x="22" y="24" text-anchor="middle" font-size="9" font-weight="700" fill="var(--text-heading)">'+pkg.progress.pct+'</text></svg><span class="stats-proj-name">'+pkg.code.replace('AI-','')+'</span></div>';
  });
  html += '</div>';

  // DRACIL rings
  if (p.mgmt) {
    var mgmtKeys = ['decisions','risks','changes','actions','issues','lessons'];
    var mgmtLabels = ['Dec','Rsk','Chg','Act','Iss','Les'];
    var mgmtColors2 = ['#569cd6','#f44336','#ff9800','#4caf50','#e91e63','#9c27b0'];
    var maxM = 1; mgmtKeys.forEach(function(k) { if ((p.mgmt[k]||0) > maxM) maxM = p.mgmt[k]; });
    html += '<div class="stats-section-title">Governance</div>';
    html += '<div class="stats-chain-grid" style="grid-template-columns:repeat(3,1fr);">';
    mgmtKeys.forEach(function(k, i) {
      var v = p.mgmt[k]||0;
      html += '<div class="stats-chain-cell" style="border-color:'+mgmtColors2[i]+';"><span class="stats-chain-code">'+mgmtLabels[i]+'</span><span class="stats-chain-pct" style="color:'+mgmtColors2[i]+';">'+v+'</span></div>';
    });
    html += '</div>';
  }

  // Phase vs Artifact completion
  var totalPhases = 0, donePhases = 0;
  p.packages.forEach(function(pkg) { totalPhases += pkg.phase.t; donePhases += pkg.phase.c; });
  var phasePct = totalPhases > 0 ? Math.round(donePhases/totalPhases*100) : 0;
  html += '<div class="stats-section-title">Completion</div>';
  html += '<div class="uxe-ds-health">';
  html += '<div class="uxe-ds-item"><div class="uxe-ds-ring"><svg viewBox="0 0 40 40"><circle cx="20" cy="20" r="16" fill="none" stroke="var(--bg-hover)" stroke-width="4"/><circle cx="20" cy="20" r="16" fill="none" stroke="#9c27b0" stroke-width="4" stroke-dasharray="'+(phasePct*1.005)+' 100.5" stroke-linecap="round" transform="rotate(-90 20 20)"/></svg><span class="uxe-ds-pct">'+phasePct+'%</span></div><span class="uxe-ds-label">Phases</span><span class="uxe-ds-count">'+donePhases+'/'+totalPhases+'</span></div>';
  html += '<div class="uxe-ds-item"><div class="uxe-ds-ring"><svg viewBox="0 0 40 40"><circle cx="20" cy="20" r="16" fill="none" stroke="var(--bg-hover)" stroke-width="4"/><circle cx="20" cy="20" r="16" fill="none" stroke="#2196f3" stroke-width="4" stroke-dasharray="'+(artPct*1.005)+' 100.5" stroke-linecap="round" transform="rotate(-90 20 20)"/></svg><span class="uxe-ds-pct">'+artPct+'%</span></div><span class="uxe-ds-label">Artifacts</span><span class="uxe-ds-count">'+doneArts+'/'+totalArts+'</span></div>';
  html += '</div>';

  el.innerHTML = html;
}

// === CHAIN TAB ===
function renderChain(project) {
  if (!project || !project.edges || !project.edges.length) { document.getElementById('chain-mermaid').innerHTML = '<div class="empty-state">No chain data</div>'; return; }
  var theme = document.documentElement.getAttribute('data-theme') === 'light' ? 'default' : 'dark';
  var lines = ['graph LR']; var nodes = {};
  project.packages.forEach(function(pkg) { var nid = pkg.code.replace('AI-','').replace('-','_'); nodes[pkg.code] = nid; lines.push('  '+nid+'["'+pkg.code+' '+(statusEmojis[pkg.status]||'')+'"]'); });
  project.edges.forEach(function(e) { var f = nodes[e.from]||e.from.replace('AI-',''); var t = nodes[e.to]||e.to.replace('AI-',''); if (e.type==='feedback') lines.push('  '+f+' -.->|'+e.label+'| '+t); else if (e.label) lines.push('  '+f+' -->|'+e.label+'| '+t); else lines.push('  '+f+' --> '+t); });
  var sm = {complete:'fill:#4caf50,stroke:#388e3c,color:#fff',active:'fill:#ff9800,stroke:#f57c00,color:#fff',pending:'fill:#e0e0e0,stroke:#bdbdbd,color:#333',blocked:'fill:#f44336,stroke:#d32f2f,color:#fff'};
  project.packages.forEach(function(pkg) { if (nodes[pkg.code]&&sm[pkg.status]) lines.push('  style '+nodes[pkg.code]+' '+sm[pkg.status]); });
  var container = document.getElementById('chain-mermaid');
  container.removeAttribute('data-processed');
  container.innerHTML = lines.join('\n');
  if (typeof mermaid !== 'undefined') { mermaid.initialize({startOnLoad:false,theme:theme,flowchart:{useMaxWidth:true,curve:'basis'}}); mermaid.init(undefined, container); }
}

// === INIT ===
function init() {
  // D should already be defined (injected by the extension host, or resolved by the loader in index.html)
  if (!D || !D.projects) {
    if (typeof window !== 'undefined' && typeof window.__dashboardEmpty === 'function') {
      window.__dashboardEmpty({ message: 'No data loaded. Standalone: data is resolved via AI-DFE <code>REGISTRY.json</code>; or load a data file below. In VS Code: run <code>DAT__ all</code> to populate the data surface.' });
    } else {
      document.querySelector('.panel-left').innerHTML = '<div class="empty-state" style="margin-top:40px;">No data loaded. Run <code>DAT__ all</code> (AI-DFE) to populate the data surface, or open via the VS Code extension.</div>';
    }
    return;
  }

  loadTheme();
  initTabs('left-tabs');
  initTabs('right-tabs');
  renderPortfolio();
  renderIdeas();
  renderStatsLeft();
  document.getElementById('footer-date').textContent = 'Updated: ' + new Date(D.generated).toLocaleDateString();

  // Auto-select first active project
  var active = D.projects.find(function(p) { return p.status === 'active'; });
  if (active) selectProject(active.id);

  // Mermaid: wait for CDN
  var attempts = 0;
  var interval = setInterval(function() {
    attempts++;
    if (typeof mermaid !== 'undefined') { clearInterval(interval); if (selectedProject) renderChain(selectedProject); }
    if (attempts > 15) clearInterval(interval);
  }, 200);
}

// VS Code mode: listen for data updates from extension
if (isVSCode) {
  window.addEventListener('message', function(event) {
    var msg = event.data;
    if (msg.type === 'updateData') { D = msg.data; init(); }
  });
}

document.addEventListener('DOMContentLoaded', init);



