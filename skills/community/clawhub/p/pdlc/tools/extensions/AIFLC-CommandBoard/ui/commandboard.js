/**
 * AIFLC Command Board — Rendering & Interaction Logic
 * Zero dependencies. Works in browser (file://) and VS Code webview.
 * v0.3.0 — Expandable cards + package family filter + category filter.
 */

var isVSCode = (typeof acquireVsCodeApi !== 'undefined');
var vscode = isVSCode ? acquireVsCodeApi() : null;
var activeFamily = 'all';
var activeCategory = 'all';

// === THEME ===
function toggleTheme() {
  var html = document.documentElement;
  var next = html.getAttribute('data-theme') === 'dark' ? 'light' : 'dark';
  html.setAttribute('data-theme', next);
  localStorage.setItem('cb-theme', next);
}
function loadTheme() {
  var saved = localStorage.getItem('cb-theme');
  if (saved) document.documentElement.setAttribute('data-theme', saved);
}

// === COPY TO CLIPBOARD ===
function copyTrigger(key, event) {
  event.stopPropagation();
  if (isVSCode) {
    vscode.postMessage({ type: 'copyTrigger', key: key });
  } else {
    navigator.clipboard.writeText(key).catch(function() {});
  }
  showToast('Copied: ' + key);
}

function copyText(text, event) {
  event.stopPropagation();
  if (isVSCode) {
    vscode.postMessage({ type: 'copyTrigger', key: text });
  } else {
    navigator.clipboard.writeText(text).catch(function() {});
  }
  showToast('Copied!');
}

function showToast(msg) {
  var toast = document.getElementById('toast');
  toast.textContent = msg;
  toast.classList.add('visible');
  setTimeout(function() { toast.classList.remove('visible'); }, 1500);
}

// === EXPAND/COLLAPSE ===
function toggleExpand(cardEl, event) {
  if (event.target.classList.contains('copy-btn') || event.target.classList.contains('copy-icon')) return;
  cardEl.classList.toggle('expanded');
}

// === RENDER: FAMILY FILTER (top-level — reserved for multi-family future) ===
function renderFamilyFilter(data) {
  var el = document.getElementById('family-filter');
  // Currently only PDLC family exists. This filter is future-proofed for when
  // additional families (e.g., EAFLC) are added. For now it shows one active option.
  var families = [
    { id: 'pdlc', name: 'PDLC' }
    // Future: { id: 'eaflc', name: 'EAFLC' }, etc.
  ];

  var html = '<span class="filter-label">Family:</span>';
  html += '<button class="family-filter-btn active" onclick="setFamilyFilter(\'all\',this)">All</button>';
  families.forEach(function(f) {
    html += '<button class="family-filter-btn' + (families.length === 1 ? ' active' : '') + '" onclick="setFamilyFilter(\'' + f.id + '\',this)">' + f.name + '</button>';
  });
  el.innerHTML = html;
}

function setFamilyFilter(family, btn) {
  activeFamily = family;
  document.querySelectorAll('.family-filter-btn').forEach(function(b) { b.classList.remove('active'); });
  btn.classList.add('active');
  applyFilter();
}

// === RENDER: CATEGORY FILTER (secondary) ===
function renderCategoryFilter(data) {
  var el = document.getElementById('category-filter');
  var html = '<span class="filter-label">Type:</span>';
  html += '<button class="filter-btn active" onclick="setCategoryFilter(\'all\',this)">All</button>';
  data.categories.forEach(function(cat) {
    html += '<button class="filter-btn" onclick="setCategoryFilter(\'' + cat.id + '\',this)">' + cat.name.replace(/ — .*/, '').replace(/ \(.*/, '') + '</button>';
  });
  el.innerHTML = html;
}

function setCategoryFilter(id, btn) {
  activeCategory = id;
  document.querySelectorAll('.filter-btn').forEach(function(b) { b.classList.remove('active'); });
  btn.classList.add('active');
  applyFilter();
}

// === FILTER LOGIC ===
function applyFilter() {
  var query = document.getElementById('search').value.toLowerCase();

  document.querySelectorAll('.category-section').forEach(function(sec) {
    var catId = sec.getAttribute('data-cat');
    var catVisible = (activeCategory === 'all' || activeCategory === catId);
    var anyCardVisible = false;

    sec.querySelectorAll('.trigger-card').forEach(function(card) {
      var text = card.getAttribute('data-search');
      var matchesSearch = !query || text.indexOf(query) !== -1;
      var visible = catVisible && matchesSearch;
      card.classList.toggle('hidden', !visible);
      if (visible) anyCardVisible = true;
    });

    sec.classList.toggle('hidden', !anyCardVisible);
  });
}

// === RENDER: GRID ===
function escHtml(str) {
  return str.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
}

function renderGrid(data) {
  var el = document.getElementById('command-grid');
  var html = '';
  data.categories.forEach(function(cat) {
    html += '<div class="category-section" data-cat="' + cat.id + '">';
    html += '<div class="category-title">' + escHtml(cat.name) + '</div>';
    html += '<div class="trigger-list">';
    cat.triggers.forEach(function(t) {
      var searchText = (t.key + ' ' + t.desc + ' ' + (t.package || '') + ' ' + (t.details ? t.details.explanation : '')).toLowerCase();
      var tier = (t.details && t.details.tier) ? t.details.tier : '';
      var pkg = t.package || '';

      html += '<div class="trigger-card" data-search="' + escHtml(searchText) + '" data-pkg="' + escHtml(pkg) + '" onclick="toggleExpand(this, event)">';

      // Header row
      html += '<div class="card-header">';
      html += '<span class="key">' + escHtml(t.key) + '</span>';
      html += '<span class="desc">' + escHtml(t.desc) + '</span>';
      if (t.package && t.package !== '—') html += '<span class="pkg">' + escHtml(t.package) + '</span>';
      if (tier) html += '<span class="tier">' + escHtml(tier) + '</span>';
      html += '<button class="copy-btn" onclick="copyTrigger(\'' + escHtml(t.key).replace(/'/g, "\\'") + '\', event)" title="Copy trigger">📋</button>';
      html += '<span class="expand-arrow">▶</span>';
      html += '</div>';

      // Expandable details
      if (t.details) {
        html += '<div class="card-details">';

        // Explanation
        html += '<div class="detail-section">';
        html += '<div class="detail-label">What it does</div>';
        html += '<div class="detail-text">' + escHtml(t.details.explanation) + '</div>';
        html += '</div>';

        // Combinations table
        if (t.details.combinations && t.details.combinations.length > 0) {
          html += '<div class="detail-section">';
          html += '<div class="detail-label">Usage Combinations</div>';
          html += '<table class="combo-table">';
          html += '<thead><tr><th>Command</th><th>What it does</th></tr></thead>';
          html += '<tbody>';
          t.details.combinations.forEach(function(c) {
            html += '<tr>';
            html += '<td><code class="combo-key" onclick="copyText(\'' + escHtml(c.usage).replace(/'/g, "\\'") + '\', event)" title="Click to copy">' + escHtml(c.usage) + '</code></td>';
            html += '<td>' + escHtml(c.meaning) + '</td>';
            html += '</tr>';
          });
          html += '</tbody></table>';
          html += '</div>';
        }

        // Sample
        if (t.details.sample) {
          html += '<div class="detail-section">';
          html += '<div class="detail-label">Example</div>';
          html += '<div class="sample-box" onclick="copyText(\'' + escHtml(t.details.sample).replace(/'/g, "\\'") + '\', event)" title="Click to copy">';
          html += '<code>' + escHtml(t.details.sample) + '</code>';
          html += '<span class="sample-copy">📋</span>';
          html += '</div>';
          html += '</div>';
        }

        html += '</div>'; // .card-details
      }

      html += '</div>'; // .trigger-card
    });
    html += '</div></div>';
  });
  el.innerHTML = html;
}

// === SEARCH ===
function initSearch() {
  document.getElementById('search').addEventListener('input', function() {
    applyFilter();
  });
}

// === DATA LOADING ===
function loadData(callback) {
  if (TRIGGERS) { callback(TRIGGERS); return; }

  try {
    var xhr = new XMLHttpRequest();
    xhr.open('GET', '../data/triggers.json', true);
    xhr.onload = function() {
      if (xhr.status === 200) {
        TRIGGERS = JSON.parse(xhr.responseText);
        callback(TRIGGERS);
      } else {
        showFallback();
      }
    };
    xhr.onerror = function() { showFallback(); };
    xhr.send();
  } catch (e) {
    showFallback();
  }
}

function showFallback() {
  document.getElementById('command-grid').innerHTML =
    '<div style="text-align:center;padding:60px;color:var(--text-secondary);">' +
    '<p>Could not load trigger data.</p>' +
    '<p style="font-size:12px;margin-top:8px;">In file:// mode, some browsers block XHR. ' +
    'Try opening via a local server or use the VS Code extension.</p></div>';
}

// === INIT ===
function init() {
  loadTheme();
  loadData(function(data) {
    renderFamilyFilter(data);
    renderCategoryFilter(data);
    renderGrid(data);
    initSearch();
  });
}

// VS Code mode: listen for data updates
if (isVSCode) {
  window.addEventListener('message', function(event) {
    var msg = event.data;
    if (msg.type === 'updateData') {
      TRIGGERS = msg.data;
      renderFamilyFilter(TRIGGERS);
      renderCategoryFilter(TRIGGERS);
      renderGrid(TRIGGERS);
    }
  });
}

document.addEventListener('DOMContentLoaded', init);
