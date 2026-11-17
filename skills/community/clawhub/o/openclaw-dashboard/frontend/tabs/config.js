
/* Config Tab — Config Viewer, File Browser, Tasks Kanban */

async function loadConfig() {
  const el = document.getElementById('configContent');
  if (!el) return;
  try {
    const health = await apiFetch('/health').catch(() => ({}));
    const caps = health.capabilities || {};
    if (!caps.configEndpoint) {
      el.innerHTML = `<div class="empty-state"><h3>Config endpoint disabled</h3><p>Read-only dashboard mode. Files remain browsable below, but /ops/config is intentionally disabled.</p></div>`;
      return;
    }
    const data = await apiFetch('/ops/config');
    applyCapabilitiesUI();
    const files = data.files || [];
    const cats = { core: '⚙️ Core Config', keys: '🔑 API Keys', personality: '🎭 Personality & Agents' };
    const grouped = {};
    files.forEach(f => {
      const cat = f.category || 'other';
      if (!grouped[cat]) grouped[cat] = [];
      grouped[cat].push(f);
    });

    let html = '';
    for (const [cat, label] of Object.entries(cats)) {
      if (!grouped[cat]) continue;
      html += `<div class="card-title" style="margin:12px 0 8px">${label}</div>`;
      for (const f of grouped[cat]) {
        const id = 'cfg-' + f.label.replace(/[^a-z0-9]/gi, '-');
        const sizeKb = (f.size / 1024).toFixed(1);
        const modified = new Date(f.modified).toLocaleString('en-US', { timeZone: 'America/Los_Angeles', month: 'short', day: 'numeric', hour: '2-digit', minute: '2-digit' });
        html += `<div class="config-file">
          <div class="config-file-header" onclick="document.getElementById('${id}').classList.toggle('open')">
            <span>${escHtml(f.label)}<span class="config-cat ${cat}">${cat}</span></span>
            <span class="config-file-meta">${sizeKb}KB · ${modified}</span>
          </div>
          <div class="config-file-body" id="${id}"><pre>${escHtml(f.content)}</pre></div>
        </div>`;
      }
    }
    el.innerHTML = html;
  } catch (e) { el.innerHTML = `<p>${escHtml(e.message)}</p>`; }
}

async function loadSkills() {
  const el = document.getElementById('skillsContent');
  if (!el) return;
  try {
    const data = await apiFetch('/skills');
    const skills = Array.isArray(data?.skills) ? data.skills : [];
    if (!skills.length) {
      el.innerHTML = `<div class="ops-ch-meta">No skills found.</div>`;
      return;
    }

    const sorted = [...skills].sort((a, b) => String(a.name || '').localeCompare(String(b.name || '')));
    const chips = sorted.map((s) => {
      const desc = s.description || s.summary || '';
      const title = `${s.name || 'unknown'}${desc ? ' — ' + desc : ''}`;
      return `<div class="pill" title="${escHtml(title)}" style="max-width:100%;overflow:hidden;text-overflow:ellipsis;white-space:nowrap">${escHtml(s.name || 'unknown')}</div>`;
    }).join('');

    el.innerHTML = `
      <div class="ops-cost-row" style="margin-bottom:10px">
        <span class="ops-cost-label">Installed</span>
        <span class="ops-cost-value">${sorted.length}</span>
      </div>
      <div class="skills-grid">${chips}</div>
    `;
  } catch (e) {
    el.innerHTML = `<div class="ops-ch-meta" style="color:var(--red)">Failed to load skills: ${escHtml(e.message)}</div>`;
  }
}

// ─── Enhanced Cron ───

async function loadFileList() {
  const sidebar = document.getElementById('fileSidebar');
  // Load memory dir files
  try {
    const data = await apiFetch('/files?path=memory/&list=true');
    memoryFiles = Array.isArray(data) ? data : (data.files || []);
  } catch(e) { memoryFiles = []; }

  sidebar.innerHTML = WORKSPACE_FILES.map(f => `
    <div class="file-item ${currentFile === f ? 'active' : ''}" onclick="selectFile('${f}')">
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/></svg>
      <span class="file-name">${f}</span>
    </div>
  `).join('') + (memoryFiles.length ? `
    <div class="file-divider"></div>
    <div class="file-sidebar-header">memory/</div>
    ${memoryFiles.map(f => {
      const path = typeof f === 'string' ? f : f.name || f.path || '';
      const name = path.split('/').pop();
      return `<div class="file-item indent ${currentFile === 'memory/' + name ? 'active' : ''}" onclick="selectFile('memory/${name}')">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/></svg>
        <span class="file-name">${escHtml(name)}</span>
      </div>`;
    }).join('')}
  ` : '');
}

async function selectFile(path) {
  currentFile = path;
  loadFileList();
  const preview = document.getElementById('mdPreview');
  const fname = document.getElementById('editorFilename');

  fname.innerHTML = `${escHtml(path)}`;
  preview.innerHTML = '<div style="text-align:center;padding:40px;color:var(--text2)"><div class="spinner"></div><p style="margin-top:12px;font-size:.84rem">Loading…</p></div>';

  try {
    const data = await apiFetch(`/files?path=${encodeURIComponent(path)}`);
    const content = typeof data === 'string' ? data : (data.content || JSON.stringify(data, null, 2));
    renderMarkdownPreview(content);
  } catch(e) {
    preview.innerHTML = `<div class="md-empty-hint"><p style="color:var(--red)">Error loading file: ${escHtml(e.message)}</p></div>`;
  }
}

function renderMarkdownPreview(content) {
  const preview = document.getElementById('mdPreview');
  if (!content || !content.trim()) {
    preview.innerHTML = '<div class="md-empty-hint"><p>This file is empty</p></div>';
    return;
  }
  try {
    if (typeof marked !== 'undefined' && marked.parse) {
      preview.innerHTML = sanitizeHtml(marked.parse(content, { breaks: true, gfm: true }));
    } else {
      preview.innerHTML = renderMarkdown(content);
    }
  } catch(e) {
    preview.innerHTML = `<pre style="white-space:pre-wrap;color:var(--text2)">${escHtml(content)}</pre>`;
  }
}

// ═══ AGENT MONITOR ═══
let agentData = null;


let allTasks = [];
let currentFilter = 'all';
let expandedTaskId = null;
let _tasksHash = '';
let _livePollingId = null;
const LIVE_POLL_MS = 15000; // was 3000, reduced to avoid excessive polling // poll every 3 seconds

function _hashTasks(tasks) {
  // Fast hash: JSON of id+status+updatedAt+notes.length for each task
  return tasks.map(t => `${t.id}|${t.status}|${t.updatedAt}|${(t.notes||[]).length}`).join(';');
}

async function loadTasks(force) {
  const list = document.getElementById('taskList');
  if (!list) return;
  try {
    const data = await apiFetch('/tasks');
    const tasks = Array.isArray(data) ? data : (data.tasks || []);
    const newHash = _hashTasks(tasks);
    // Skip re-render if nothing changed (unless forced)
    if (!force && newHash === _tasksHash) return;
    _tasksHash = newHash;
    allTasks = tasks;
    const taskCountEl = document.getElementById('taskCount');
    if (taskCountEl) taskCountEl.textContent = allTasks.length;
    renderTasks();
    // If detail modal is open, refresh it from the read-only source.
    if (detailTaskId) {
      const updated = allTasks.find(t => t.id === detailTaskId);
      if (updated) openDetailModal(detailTaskId);
    }
    // Flash the live indicator on data change
    _flashLiveIndicator();
  } catch(e) {
    list.innerHTML = `<div class="empty-state"><svg viewBox="0 0 80 80"><circle cx="40" cy="40" r="36" fill="none" stroke="currentColor" stroke-width="2"/><path d="M28 28l24 24M52 28L28 52" stroke="currentColor" stroke-width="2"/></svg><h3>Unable to Load Tasks</h3><p>${escHtml(e.message)}</p><button class="action-btn primary" onclick="loadTasks(true)" style="margin:0 auto">Retry</button></div>`;
  }
}

function _flashLiveIndicator() {
  const el = document.getElementById('liveIndicator');
  if (!el) return;
  el.classList.add('flash');
  setTimeout(() => el.classList.remove('flash'), 600);
}

function startLivePolling() {
  if (_livePollingId) return;
  _livePollingId = setInterval(() => loadTasks(false), LIVE_POLL_MS);
  const el = document.getElementById('liveIndicator');
  if (el) el.classList.add('active');
}

function stopLivePolling() {
  if (_livePollingId) { clearInterval(_livePollingId); _livePollingId = null; }
  const el = document.getElementById('liveIndicator');
  if (el) el.classList.remove('active');
}

function toggleLivePolling() {
  if (_livePollingId) { stopLivePolling(); toast('Live updates paused', 'info'); }
  else { startLivePolling(); toast('Live updates enabled', 'info'); }
}

function renderTasks() {
  const list = document.getElementById('taskList');
  if (!list) return;
  const search = (document.getElementById('taskSearch').value || '').toLowerCase();
  let filtered = allTasks;
  if (currentFilter !== 'all') filtered = filtered.filter(t => (t.status || 'new') === currentFilter);
  if (search) filtered = filtered.filter(t => (t.title || '').toLowerCase().includes(search) || (t.description || '').toLowerCase().includes(search));

  if (filtered.length === 0) {
    list.innerHTML = `<div class="empty-state">
      <svg viewBox="0 0 80 80"><rect x="16" y="12" width="48" height="56" rx="6" fill="none" stroke="currentColor" stroke-width="1.5"/><line x1="28" y1="28" x2="52" y2="28" stroke="currentColor" stroke-width="1.5"/><line x1="28" y1="38" x2="48" y2="38" stroke="currentColor" stroke-width="1.5"/><line x1="28" y1="48" x2="44" y2="48" stroke="currentColor" stroke-width="1.5"/><circle cx="24" cy="28" r="2" fill="currentColor"/><circle cx="24" cy="38" r="2" fill="currentColor"/><circle cx="24" cy="48" r="2" fill="currentColor"/></svg>
      <h3>${currentFilter !== 'all' ? 'No matching tasks' : 'No tasks yet'}</h3>
      <p>${currentFilter !== 'all' ? 'Try a different filter.' : 'Create and update tasks through Discord or the authenticated OpenClaw CLI.'}</p>
    </div>`;
    return;
  }

  list.innerHTML = filtered.map((task, i) => {
    const status = task.status || 'new';
    const priority = task.priority || 'medium';
    const isExpanded = expandedTaskId === task.id;
    const notes = task.notes || [];
    const date = task.createdAt ? new Date(task.createdAt).toLocaleDateString('en-US', { month: 'short', day: 'numeric' }) : '';
    const dueDate = task.dueDate ? new Date(task.dueDate).toLocaleDateString('en-US', { month: 'short', day: 'numeric' }) : '';
    return `<div class="glass-card task-card status-${status} ${isExpanded ? 'expanded' : ''}" onclick="toggleTask('${task.id}')" style="animation:cardIn .4s ease backwards;animation-delay:${i * 0.05}s">
      <div class="task-header">
        <span class="task-title">${escHtml(task.title || 'Untitled')}</span>
        <span class="badge badge-${status}">${statusLabel(status)}</span>
        <span class="badge badge-priority ${priority}">${priority}</span>
      </div>
      <div class="task-meta">
        ${task.assignee ? `<span>👤 ${escHtml(task.assignee)}</span>` : ''}
        ${date ? `<span>📅 ${date}</span>` : ''}
        ${dueDate ? `<span>⏰ Due ${dueDate}</span>` : ''}
        ${notes.length ? `<span>📝 ${notes.length} note${notes.length > 1 ? 's' : ''}</span>` : ''}
        ${task.content ? '<span>📄 Content</span>' : ''}
      </div>
      <div class="task-body" onclick="event.stopPropagation()">
        ${task.description ? `<div class="task-description">${renderMarkdown(task.description)}</div>` : ''}
        ${task.content ? `<div class="task-content-preview" onclick="event.stopPropagation();this.classList.toggle('expanded')">
          <div class="task-content-label"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/><line x1="16" y1="13" x2="8" y2="13"/><line x1="16" y1="17" x2="8" y2="17"/><polyline points="10 9 9 9 8 9"/></svg> Content</div>
          <div class="task-content-md">${renderFullMarkdown(task.content)}</div>
        </div>` : ''}
        <div class="notes-section">
          <div class="notes-title">Notes</div>
          <div class="notes-list">
            ${notes.length === 0 ? '<div style="font-size:.8rem;color:var(--text2);padding:4px 0 4px 16px;border-left:2px solid var(--border)">No notes yet</div>' : notes.map(n => `
              <div class="note-item">
                <span class="note-time">${n.createdAt ? new Date(n.createdAt).toLocaleString('en-US', { month:'short', day:'numeric', hour:'2-digit', minute:'2-digit' }) : ''}</span>
                <span class="note-text">${escHtml(n.text || n.content || '')}</span>
              </div>
            `).join('')}
          </div>
          <div class="read-only-notice">Task changes and notes are managed through Discord or the authenticated OpenClaw CLI.</div>
        </div>
      </div>
    </div>`;
  }).join('');
}

function statusLabel(s) {
  return { 'new': 'New', 'in-progress': 'In Progress', 'done': 'Done', 'failed': 'Failed' }[s] || s;
}

window.escHtml = window.escHtml || function escHtml(s) {
  const d = document.createElement('div');
  d.textContent = s;
  return d.innerHTML;
}

function toggleTask(id) {
  openDetailModal(id);
}

// Filters (guarded for Ops view)
const _statusFilters = document.getElementById('statusFilters');
if (_statusFilters) {
  _statusFilters.addEventListener('click', e => {
    const btn = e.target.closest('.filter-btn');
    if (!btn) return;
    document.querySelectorAll('#statusFilters .filter-btn').forEach(b => b.classList.remove('active'));
    btn.classList.add('active');
    currentFilter = btn.dataset.filter;
    renderTasks();
  });
}

const _taskSearch = document.getElementById('taskSearch');
if (_taskSearch) {
  _taskSearch.addEventListener('input', () => {
    renderTasks();
  });
}

// ═══ KANBAN VIEW ═══
let taskView = localStorage.getItem('taskView') || 'list';

function setTaskView(view) {
  taskView = view;
  localStorage.setItem('taskView', view);
  document.querySelectorAll('#taskViewToggle button').forEach(b => b.classList.toggle('active', b.dataset.view === view));
  const listEl = document.getElementById('taskList');
  const kanbanEl = document.getElementById('kanbanBoard');
  const filtersEl = document.getElementById('statusFilters');
  if (!listEl || !kanbanEl || !filtersEl) return;
  if (view === 'kanban') {
    listEl.style.display = 'none';
    kanbanEl.style.display = '';
    filtersEl.style.display = 'none';
    renderKanban();
  } else {
    listEl.style.display = '';
    kanbanEl.style.display = 'none';
    filtersEl.style.display = '';
    renderTasks();
  }
}

const KANBAN_COLUMNS = [
  { status: 'new', label: 'New' },
  { status: 'in-progress', label: 'In Progress' },
  { status: 'done', label: 'Done' },
  { status: 'failed', label: 'Failed' }
];

function renderKanban() {
  const board = document.getElementById('kanbanBoard');
  const search = (document.getElementById('taskSearch').value || '').toLowerCase();
  let filtered = allTasks;
  if (search) filtered = filtered.filter(t => (t.title || '').toLowerCase().includes(search) || (t.description || '').toLowerCase().includes(search));

  board.innerHTML = KANBAN_COLUMNS.map(col => {
    const colTasks = filtered.filter(t => (t.status || 'new') === col.status);
    return `<div class="kanban-column" data-status="${col.status}">
      <div class="kanban-col-header">
        <div class="kanban-col-title">
          <span class="col-dot ${col.status}"></span>
          ${col.label}
        </div>
        <span class="kanban-col-count">${colTasks.length}</span>
      </div>
      <div class="kanban-col-body${colTasks.length === 0 ? ' empty-drop' : ''}">
        ${colTasks.length === 0
          ? '<div class="drop-hint">No tasks</div>'
          : colTasks.map(task => renderKanbanCard(task)).join('')}
      </div>
    </div>`;
  }).join('');

  // Add mobile horizontal scroll class
  if (window.innerWidth <= 768) board.classList.add('horizontal-scroll');
  else board.classList.remove('horizontal-scroll');
}

function renderKanbanCard(task) {
  const status = task.status || 'new';
  const priority = task.priority || 'medium';
  return `<div class="kanban-card status-${status}"
               data-task-id="${task.id}"
               onclick="kanbanCardClick('${task.id}')">
    <div class="kanban-card-title">${escHtml(task.title || 'Untitled')}</div>
    <div class="kanban-card-footer">
      <span class="badge badge-priority ${priority}">${priority}</span>
      ${task.notes && task.notes.length ? `<span style="font-size:.68rem;color:var(--text2)">📝${task.notes.length}</span>` : ''}
      ${task.assignee ? `<span class="kanban-card-assignee">👤 ${escHtml(task.assignee)}</span>` : ''}
    </div>
  </div>`;
}

function kanbanCardClick(taskId) {
  openDetailModal(taskId);
}

// ═══ TASK DETAIL MODAL ═══
let detailTaskId = null;

function openDetailModal(taskId) {
  const task = allTasks.find(t => t.id === taskId);
  if (!task) return;
  detailTaskId = taskId;

  const status = task.status || 'new';
  const priority = task.priority || 'medium';
  const created = task.createdAt ? new Date(task.createdAt) : null;
  const updated = task.updatedAt ? new Date(task.updatedAt) : null;
  const due = task.dueDate ? new Date(task.dueDate) : null;
  const notes = task.notes || [];

  // Separate agent output notes from status/regular notes
  const statusNotes = [];
  const outputNotes = [];
  const regularNotes = [];
  notes.forEach(n => {
    const txt = n.text || n.content || '';
    if (txt.startsWith('Status changed')) statusNotes.push(n);
    else if (txt.length > 150) outputNotes.push(n);
    else regularNotes.push(n);
  });

  // Header
  document.getElementById('detailStatusRow').innerHTML = `
    <span class="badge badge-${status}">${statusLabel(status)}</span>
    <span class="badge badge-priority ${priority}">${priority}</span>
    ${task.source ? `<span class="badge" style="background:rgba(139,148,158,0.1);color:var(--text2);border:1px solid var(--border)">${escHtml(task.source)}</span>` : ''}
  `;
  document.getElementById('detailTitle').textContent = task.title || 'Untitled';
  document.getElementById('detailMeta').innerHTML = `
    ${task.assignee ? `<span>👤 ${escHtml(task.assignee)}</span>` : ''}
    ${created ? `<span>📅 Created ${created.toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' })}</span>` : ''}
    ${updated ? `<span>🔄 Updated ${timeAgo(updated)}</span>` : ''}
    ${due ? `<span>⏰ Due ${due.toLocaleDateString('en-US', { month: 'short', day: 'numeric' })}</span>` : ''}
  `;

  // Body
  let bodyHtml = '';

  // Description section
  if (task.description) {
    bodyHtml += `
    <div class="detail-section">
      <div class="detail-section-title" onclick="this.classList.toggle('collapsed')">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M6 9l6 6 6-6"/></svg>
        Description
      </div>
      <div class="detail-section-content">
        <div class="detail-description">${renderMarkdown(task.description)}</div>
      </div>
    </div>`;
  }

  // Content section (rich markdown field)
  bodyHtml += `
  <div class="detail-content-section">
    <div class="detail-content-area" id="detailContentArea">
      <div class="detail-content-header">
        <span class="content-label">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/><line x1="16" y1="13" x2="8" y2="13"/><line x1="16" y1="17" x2="8" y2="17"/><polyline points="10 9 9 9 8 9"/></svg>
          Content <span style="font-weight:400;font-size:.68rem;color:var(--text2);letter-spacing:0;text-transform:none;margin-left:4px">Markdown</span>
        </span>
        <span class="card-sub">Read-only</span>
      </div>
      <div class="detail-content-md" id="detailContentMd">
        ${task.content ? renderFullMarkdown(task.content) : `<div class="detail-content-empty">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/></svg>
          No content available
        </div>`}
      </div>
    </div>
  </div>`;

  // Agent Output section (long notes = agent results)
  if (outputNotes.length > 0) {
    bodyHtml += `
    <div class="detail-section">
      <div class="detail-section-title" onclick="this.classList.toggle('collapsed')">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M6 9l6 6 6-6"/></svg>
        Agent Output <span style="font-weight:400;font-size:.7rem;color:var(--accent2)">${outputNotes.length} result${outputNotes.length > 1 ? 's' : ''}</span>
      </div>
      <div class="detail-section-content">
        ${outputNotes.map((n, i) => {
          const txt = n.text || n.content || '';
          const time = n.timestamp || n.createdAt;
          const escaped = txt.replace(/\\/g, '\\\\').replace(/'/g, "\\'").replace(/\n/g, '\\n').replace(/\r/g, '');
          return `<div class="detail-output" style="${i > 0 ? 'margin-top:10px' : ''}">
            <div class="detail-output-header">
              <span>🤖 Output${time ? ' · ' + new Date(time).toLocaleString('en-US', { month:'short', day:'numeric', hour:'2-digit', minute:'2-digit' }) : ''}</span>
              <button class="detail-output-copy" onclick="copyOutput(this, '${escaped}')">Copy</button>
            </div>
            <div class="detail-output-body">${renderMarkdown(txt)}</div>
          </div>`;
        }).join('')}
      </div>
    </div>`;
  }

  // Activity / Comments section (regular + status notes combined)
  const activityNotes = [...regularNotes, ...statusNotes].sort((a, b) => {
    const ta = new Date(a.timestamp || a.createdAt || 0).getTime();
    const tb = new Date(b.timestamp || b.createdAt || 0).getTime();
    return tb - ta;
  });

  bodyHtml += `
  <div class="detail-section">
    <div class="detail-section-title" onclick="this.classList.toggle('collapsed')">
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M6 9l6 6 6-6"/></svg>
      Activity & Comments <span style="font-weight:400;font-size:.7rem;color:var(--text2)">${activityNotes.length}</span>
    </div>
    <div class="detail-section-content">
      <div class="detail-notes" id="detailNotes">
        ${activityNotes.length === 0 ? '<div style="font-size:.82rem;color:var(--text2);padding:12px 0">No activity yet</div>' : activityNotes.map(n => {
          const txt = n.text || n.content || '';
          const time = n.timestamp || n.createdAt;
          const isStatus = txt.startsWith('Status changed');
          const isLong = txt.length > 200;
          const noteId = 'dn-' + Math.random().toString(36).slice(2, 8);
          return `<div class="detail-note ${isStatus ? 'is-status' : ''}">
            <div class="detail-note-time">${time ? new Date(time).toLocaleString('en-US', { month:'short', day:'numeric', hour:'2-digit', minute:'2-digit' }) : ''}</div>
            <div class="detail-note-text ${isLong ? 'truncated' : ''}" id="${noteId}">${escHtml(txt)}</div>
            ${isLong ? `<span class="detail-note-expand" onclick="toggleNoteExpand('${noteId}', this)">Show more</span>` : ''}
          </div>`;
        }).join('')}
      </div>
      <div class="read-only-notice">Comments and status changes are managed through Discord or the authenticated OpenClaw CLI.</div>
    </div>
  </div>`;

  document.getElementById('detailBody').innerHTML = bodyHtml;

  // Actions footer
  document.getElementById('detailActions').innerHTML = `
    <span class="card-sub">Read-only task view</span>
  `;

  document.getElementById('detailModal').classList.add('show');
}

function closeDetailModal() {
  document.getElementById('detailModal').classList.remove('show');
  detailTaskId = null;
}

function toggleNoteExpand(noteId, btn) {
  const el = document.getElementById(noteId);
  if (!el) return;
  el.classList.toggle('truncated');
  btn.textContent = el.classList.contains('truncated') ? 'Show more' : 'Show less';
}

function copyOutput(btn, text) {
  navigator.clipboard.writeText(text).then(() => {
    btn.textContent = 'Copied!';
    setTimeout(() => { btn.textContent = 'Copy'; }, 2000);
  }).catch(() => toast('Copy failed', 'error'));
}

function timeAgo(date) {
  const s = Math.floor((Date.now() - date.getTime()) / 1000);
  if (s < 60) return 'just now';
  if (s < 3600) return Math.floor(s / 60) + 'm ago';
  if (s < 86400) return Math.floor(s / 3600) + 'h ago';
  return Math.floor(s / 86400) + 'd ago';
}

document.getElementById('detailModal').addEventListener('click', e => {
  if (e.target === e.currentTarget) closeDetailModal();
});

// Restore view on load
if (taskView === 'kanban') {
  document.querySelectorAll('#taskViewToggle button').forEach(b => b.classList.toggle('active', b.dataset.view === 'kanban'));
}

// ═══ DOCUMENTS ═══
const WORKSPACE_FILES = ['MEMORY.md', 'SOUL.md', 'USER.md', 'AGENTS.md', 'TOOLS.md', 'IDENTITY.md', 'HEARTBEAT.md'];
let currentFile = null;
let memoryFiles = [];
