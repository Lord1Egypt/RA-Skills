/* Offline-only Harness Doctor interactions. No fetch, network, or clipboard. */
(function () {
  "use strict";

  var data = window.HKW_SCORECARD_DATA;
  var activeMode = "overview";
  var selectedId = null;

  function byId(id) {
    return document.getElementById(id);
  }

  function escapeHtml(value) {
    return String(value == null ? "" : value).replace(/[&<>"']/g, function (character) {
      return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[character];
    });
  }

  function statusLabel(status) {
    return status === "pass" ? "通过" : status === "partial" ? "部分" : "失败";
  }

  function setDecisionClass(node, decision) {
    if (!node) return;
    node.className = "decision " + (String(decision || "").toLowerCase() === "ready" ? "ready" : String(decision || "").toLowerCase() === "blocked" ? "blocked" : "conditional");
  }

  function renderHeader() {
    var score = data.score || {};
    var maturity = score.maturity || {};
    byId("scoreValue").textContent = score.value;
    byId("decisionValue").textContent = score.decision || "CONDITIONAL";
    setDecisionClass(byId("decisionValue"), score.decision);
    byId("maturityValue").textContent = maturity.name || "—";
    byId("confidenceValue").textContent = score.confidence || 0;
    byId("confidenceBar").style.width = Math.max(0, Math.min(100, score.confidence || 0)) + "%";
    byId("generatedAt").textContent = String(data.generatedAt || "").replace(/-/g, ".");
    byId("localChecks").textContent = data.executions[0] ? data.executions[0].governanceCounts : "—";
    byId("ciChecks").textContent = data.executions[1] ? data.executions[1].governanceCounts : "—";
    byId("hostUnknown").textContent = (data.hosts || []).filter(function (host) { return host.smokeTest === "unknown"; }).length;
  }

  function renderTabs() {
    Array.prototype.forEach.call(document.querySelectorAll(".mode-tab"), function (tab) {
      var active = tab.getAttribute("data-mode") === activeMode;
      tab.classList.toggle("active", active);
      tab.setAttribute("aria-selected", String(active));
    });
  }

  function renderOverview() {
    var items = data.dimensions || [];
    if (!selectedId || !items.some(function (item) { return item.id === selectedId; })) selectedId = items[0] ? items[0].id : null;
    var list = items.map(function (item) {
      var percentage = item.weight ? Math.round(item.earned / item.weight * 100) : 0;
      var status = item.status || "partial";
      return '<button class="dimension-item state-' + escapeHtml(status) + (item.id === selectedId ? " selected" : "") + '" type="button" data-dimension="' + escapeHtml(item.id) + '" aria-pressed="' + (item.id === selectedId) + '">' +
        '<span class="dimension-name"><i></i>' + escapeHtml(item.name) + '</span>' +
        '<span class="dimension-score">' + item.earned + "/" + item.weight + '</span>' +
        '<span class="dimension-meter"><i style="width:' + percentage + '%"></i></span>' +
        '</button>';
    }).join("");
    var selected = items.find(function (item) { return item.id === selectedId; });
    var evidence = selected ? selected.evidence || [] : [];
    var evidenceHtml = selected ?
      '<span class="evidence-status status-' + escapeHtml(selected.status) + '">' + statusLabel(selected.status) + '</span>' +
      '<h3>' + escapeHtml(selected.name) + '</h3>' +
      '<p>' + escapeHtml(selected.description || "暂无说明") + '</p>' +
      '<div class="evidence-label">证据引用</div><ul class="evidence-list">' + evidence.map(function (entry) { return '<li>' + escapeHtml(entry) + '</li>'; }).join("") + '</ul>' :
      '<p class="empty-state">选择一个维度查看证据</p>';
    byId("viewRoot").innerHTML = '<section class="section-block"><div class="section-title"><strong>12 个维度</strong><span>点击查看证据</span></div><div class="dimension-list">' + list + '</div></section>' +
      '<section class="evidence-card"><div class="section-title"><strong>证据台账</strong><span>FILE · LINE · EXIT</span></div><div class="evidence-body">' + evidenceHtml + '</div></section>';
    bindDimensionButtons();
  }

  function renderExecutions() {
    var executions = data.executions || [];
    var cards = executions.map(function (execution) {
      var passed = execution.passed && execution.exitCode === 0;
      return '<article class="execution-card"><div class="execution-top"><span class="execution-status ' + (passed ? "passed" : "failed") + '">' + (passed ? "PASS" : "FAIL") + '</span><strong>' + escapeHtml(execution.label) + '</strong><span class="execution-exit">exit ' + escapeHtml(execution.exitCode) + '</span></div>' +
        '<code>' + escapeHtml(execution.command) + '</code><div class="execution-meta"><span>治理检查 <b>' + escapeHtml(execution.governanceCounts) + '</b></span><span>耗时 <b>' + escapeHtml(execution.durationSeconds) + 's</b></span></div></article>';
    }).join("");
    var hosts = (data.hosts || []).map(function (host) {
      return '<div class="host-row"><span><i class="host-dot"></i>' + escapeHtml(host.short || host.host) + '</span><strong class="unknown">' + escapeHtml(String(host.smokeTest || "unknown").toUpperCase()) + '</strong></div>';
    }).join("");
    byId("viewRoot").innerHTML = '<section class="section-block"><div class="section-title"><strong>执行轨迹</strong><span>保留退出码</span></div><div class="execution-list">' + cards + '</div></section>' +
      '<section class="evidence-card"><div class="section-title"><strong>宿主矩阵</strong><span>配置存在 ≠ 已触发</span></div><div class="host-list">' + hosts + '</div></section>';
  }

  function renderProfile() {
    var profile = data.profile || {};
    var score = profile.score || {};
    var controls = profile.controls || [];
    var rows = controls.map(function (control) {
      var percentage = control.weight ? Math.round(control.earned / control.weight * 100) : 0;
      return '<div class="profile-row"><div><span>' + escapeHtml(control.name) + '</span><b>' + control.earned + "/" + control.weight + '</b></div><i><em style="width:' + percentage + '%"></em></i></div>';
    }).join("");
    byId("viewRoot").innerHTML = '<section class="profile-hero"><div><span class="profile-kicker">DOMAIN PROFILE</span><h3>' + escapeHtml(profile.name) + '</h3><p>策略声明可以帮助定位领域边界，但不能替代运行证据或人工凭证。</p></div><strong>' + score.value + '<small>/' + score.max + '</small></strong></section>' +
      '<section class="section-block"><div class="section-title"><strong>内容治理控制项</strong><span>策略证据</span></div><div class="profile-list">' + rows + '</div></section>';
  }

  function bindDimensionButtons() {
    Array.prototype.forEach.call(document.querySelectorAll("[data-dimension]"), function (button) {
      button.addEventListener("click", function () {
        selectedId = button.getAttribute("data-dimension");
        renderOverview();
      });
    });
  }

  function renderView() {
    renderTabs();
    if (activeMode === "executions") renderExecutions();
    else if (activeMode === "profile") renderProfile();
    else renderOverview();
  }

  function bindTabs() {
    Array.prototype.forEach.call(document.querySelectorAll(".mode-tab"), function (tab) {
      tab.addEventListener("click", function () {
        activeMode = tab.getAttribute("data-mode") || "overview";
        selectedId = null;
        renderView();
      });
    });
  }

  renderHeader();
  bindTabs();
  renderView();
}());
