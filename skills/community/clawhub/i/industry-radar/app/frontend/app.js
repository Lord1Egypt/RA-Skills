/*
 * app.js — 智汇简报 IndustryRadar 前端控制台（Vue 3，离线运行）。
 * 全部交互通过 /api/* 调用 FastAPI 后端；无任何外部 CDN 依赖。
 */
(function () {
  "use strict";
  var Vue = window.Vue;
  var ref = Vue.ref, reactive = Vue.reactive, computed = Vue.computed, onMounted = Vue.onMounted;

  var TOKEN_KEY = "ir_token";
  var USER_KEY = "ir_user";

  /* ------------------------------------------------ HTTP 封装 */
  function api(path, opts) {
    opts = opts || {};
    var headers = Object.assign({ "Content-Type": "application/json" }, opts.headers || {});
    var t = localStorage.getItem(TOKEN_KEY);
    if (t) headers["Authorization"] = "Bearer " + t;
    return fetch("/api" + path, Object.assign({}, opts, { headers: headers })).then(function (r) {
      var ct = r.headers.get("content-type") || "";
      var parse = ct.indexOf("application/json") >= 0 ? r.json() : r.text();
      return parse.then(function (data) {
        if (!r.ok) {
          var msg = (data && data.detail) ? data.detail : ("请求失败 (" + r.status + ")");
          if (typeof msg !== "string") msg = JSON.stringify(msg);
          var err = new Error(msg);
          err.status = r.status;
          throw err;
        }
        return data;
      });
    });
  }

  function fmtTime(s) { return s ? String(s).replace("T", " ").slice(0, 16) : "—"; }

  var app = Vue.createApp({
    setup: function () {
      /* -------------------------------------- 基础状态 */
      /* 支持深链接登录：?token=xxx&user=yyy&view=reader&sub=1（便于分享与自动化演示） */
      var qs = new URLSearchParams(location.search);
      if (qs.get("token")) {
        localStorage.setItem(TOKEN_KEY, qs.get("token"));
        if (qs.get("user")) localStorage.setItem(USER_KEY, qs.get("user"));
        history.replaceState(null, "", location.pathname);
      }
      var initView = qs.get("view") || "";
      var initSub = qs.get("sub") || "";
      var token = ref(localStorage.getItem(TOKEN_KEY) || "");
      var username = ref(localStorage.getItem(USER_KEY) || "");
      var authed = computed(function () { return !!token.value; });
      var view = ref("dashboard");
      var toasts = ref([]);
      var busy = ref(false);

      var config = ref({ llm_enabled: false, mode: "", version: "" });
      var sources = ref([]);
      var subs = ref([]);
      var dash = ref({ subscription_count: 0, briefing_count: 0, article_count: 0, llm_enabled: false });

      function toast(msg, type) {
        var id = Date.now() + Math.random();
        toasts.value.push({ id: id, msg: msg, type: type || "" });
        setTimeout(function () {
          toasts.value = toasts.value.filter(function (x) { return x.id !== id; });
        }, 3800);
      }

      /* -------------------------------------- 登录 */
      var loginForm = reactive({ username: "demo", password: "demo" });
      var loginErr = ref("");

      function doLogin() {
        loginErr.value = "";
        busy.value = true;
        api("/login", { method: "POST", body: JSON.stringify(loginForm) })
          .then(function (d) {
            token.value = d.token;
            username.value = d.username;
            localStorage.setItem(TOKEN_KEY, d.token);
            localStorage.setItem(USER_KEY, d.username);
            toast("登录成功", "ok");
            return loadAll();
          })
          .catch(function (e) { loginErr.value = e.message; })
          .finally(function () { busy.value = false; });
      }

      function doLogout() {
        token.value = ""; username.value = "";
        localStorage.removeItem(TOKEN_KEY); localStorage.removeItem(USER_KEY);
        view.value = "dashboard";
      }

      /* -------------------------------------- 加载数据 */
      function loadConfig() {
        return api("/config").then(function (d) { config.value = d; });
      }
      function loadSources() {
        return api("/sources").then(function (d) { sources.value = d.sources || []; });
      }
      function loadSubs() {
        return api("/subscriptions").then(function (d) { subs.value = d.subscriptions || []; });
      }
      function loadDash() {
        return api("/dashboard").then(function (d) { dash.value = d; });
      }
      function loadAll() {
        return Promise.all([loadConfig(), loadSources(), loadSubs(), loadDash(), loadCustoms()]);
      }

      /* -------------------------------------- 订阅管理 */
      var subModal = ref(false);
      var subEditing = ref(false);
      var subForm = reactive({ id: null, name: "", industry_kw: "", tech_kw: "", extra_kw: "", sources: [], frequency: "weekly", style: "standard" });

      function resetSubForm() {
        subForm.id = null; subForm.name = ""; subForm.industry_kw = "";
        subForm.tech_kw = ""; subForm.extra_kw = ""; subForm.sources = []; subForm.frequency = "weekly"; subForm.style = "standard";
      }
      function openNewSub() { resetSubForm(); subEditing.value = false; subModal.value = true; }
      function openEditSub(s) {
        subForm.id = s.id; subForm.name = s.name;
        subForm.industry_kw = s.industry_kw; subForm.tech_kw = s.tech_kw;
        subForm.extra_kw = s.extra_kw || "";
        subForm.sources = parseSources(s.sources_json);
        subForm.frequency = s.frequency || "weekly";
        subForm.style = s.style || "standard";
        subEditing.value = true; subModal.value = true;
      }
      function parseSources(json) {
        try { var a = JSON.parse(json || "[]"); return Array.isArray(a) ? a : []; } catch (e) { return []; }
      }
      function saveSub() {
        if (!subForm.name || !subForm.industry_kw || !subForm.tech_kw) {
          toast("名称 / 行业词 / 技术词均为必填", "err"); return;
        }
        var payload = {
          name: subForm.name, industry_kw: subForm.industry_kw, tech_kw: subForm.tech_kw,
          extra_kw: subForm.extra_kw, sources: subForm.sources, frequency: subForm.frequency,
          style: subForm.style || "standard",
        };
        busy.value = true;
        var p = subEditing.value
          ? api("/subscriptions/" + subForm.id, { method: "PUT", body: JSON.stringify(payload) })
          : api("/subscriptions", { method: "POST", body: JSON.stringify(payload) });
        p.then(function () {
          toast(subEditing.value ? "已更新订阅" : "已创建订阅", "ok");
          subModal.value = false;
          return Promise.all([loadSubs(), loadDash()]);
        }).catch(function (e) { toast(e.message, "err"); })
          .finally(function () { busy.value = false; });
      }
      function deleteSub(s) {
        if (!window.confirm("确认删除订阅「" + s.name + "」？其历史简报也会一并删除。")) return;
        busy.value = true;
        api("/subscriptions/" + s.id, { method: "DELETE" })
          .then(function () { toast("已删除", "ok"); return Promise.all([loadSubs(), loadDash()]); })
          .catch(function (e) { toast(e.message, "err"); })
          .finally(function () { busy.value = false; });
      }
      function toggleSub(s) {
        api("/subscriptions/" + s.id, { method: "PUT", body: JSON.stringify({ enabled: s.enabled ? 0 : 1 }) })
          .then(function () { toast(s.enabled ? "已暂停" : "已启用", "ok"); return loadSubs(); })
          .catch(function (e) { toast(e.message, "err"); });
      }
      function runSub(s) {
        busy.value = true;
        toast("正在采集与生成，请稍候…");
        api("/subscriptions/" + s.id + "/run", { method: "POST" })
          .then(function (d) {
            var st = d.stats || {};
            toast("简报生成完成：采集 " + (st.collected || 0) + " 篇 / 入选 " + (st.total_articles || 0) + " 篇", "ok");
            return Promise.all([loadSubs(), loadDash()]);
          })
          .catch(function (e) { toast("生成失败：" + e.message, "err"); })
          .finally(function () { busy.value = false; });
      }

      /* -------------------------------------- 关键词预览 */
      var previewModal = ref(false);
      var previewForm = reactive({ industry_kw: "", tech_kw: "", extra_kw: "", sources: [] });
      var previewMd = ref("");
      var previewStats = ref(null);
      var previewDone = ref(false);
      var previewRendered = computed(function () {
        return previewMd.value && window.renderMarkdown ? window.renderMarkdown(previewMd.value) : "";
      });

      function openPreview() {
        previewForm.industry_kw = ""; previewForm.tech_kw = "";
        previewForm.extra_kw = ""; previewForm.sources = [];
        previewMd.value = ""; previewStats.value = null; previewDone.value = false;
        previewModal.value = true;
      }
      function doPreview() {
        if (!previewForm.industry_kw || !previewForm.tech_kw) { toast("请填写行业词与技术词", "err"); return; }
        busy.value = true;
        api("/preview", { method: "POST", body: JSON.stringify(previewForm) })
          .then(function (d) {
            previewMd.value = d.markdown || "";
            previewStats.value = d.stats || {};
            previewDone.value = true;
          })
          .catch(function (e) { toast(e.message, "err"); })
          .finally(function () { busy.value = false; });
      }

      /* -------------------------------------- 简报阅读 */
      var readerSub = ref(null);
      var briefings = ref([]);
      var currentBriefing = ref(null);
      var articles = ref([]);
      var trend = ref({ series: [], sources: [] });
      var readerLoading = ref(false);

      var renderedMd = computed(function () {
        var b = currentBriefing.value;
        return b && window.renderMarkdown ? window.renderMarkdown(b.markdown || "") : "";
      });

      function openReader(s) {
        readerSub.value = s;
        view.value = "reader";
        currentBriefing.value = null;
        readerLoading.value = true;
        Promise.all([
          api("/briefings?subscription_id=" + s.id),
          api("/trend?subscription_id=" + s.id),
          api("/articles?subscription_id=" + s.id + "&limit=50"),
        ]).then(function (res) {
          briefings.value = res[0].briefings || [];
          trend.value = res[1];
          articles.value = res[2].articles || [];
          if (briefings.value.length) selectBriefing(briefings.value[0]);
        }).catch(function (e) { toast(e.message, "err"); })
          .finally(function () { readerLoading.value = false; });
      }

      function selectBriefing(b) {
        readerLoading.value = true;
        api("/briefings/" + b.id)
          .then(function (d) { currentBriefing.value = d; })
          .catch(function (e) { toast(e.message, "err"); })
          .finally(function () { readerLoading.value = false; });
      }

      function downloadBriefing(b) {
        var t = localStorage.getItem(TOKEN_KEY);
        fetch("/api/briefings/" + b.id + "/export?fmt=md", { headers: { Authorization: "Bearer " + t } })
          .then(function (r) { if (!r.ok) throw new Error("导出失败"); return r.blob(); })
          .then(function (blob) {
            var url = URL.createObjectURL(blob);
            var a = document.createElement("a");
            a.href = url;
            a.download = "智汇简报_" + b.id + ".md";
            document.body.appendChild(a); a.click(); document.body.removeChild(a);
            URL.revokeObjectURL(url);
            toast("已导出 Markdown", "ok");
          })
          .catch(function (e) { toast(e.message, "err"); });
      }

      function statsOf(b) {
        try { return JSON.parse(b.stats_json || "{}"); } catch (e) { return {}; }
      }
      function statValue(b, key) { var s = statsOf(b); return s[key] != null ? s[key] : "—"; }

      var CAT_NAME = { tech: "科技", business: "商业", finance: "财经", research: "学术" };
      function catName(c) { return CAT_NAME[c] || c || "其他"; }
      // 订阅实际生效的来源名（留空=全部启用源）；cs:<id> 指向用户自己的自定义源
      function srcList(s) {
        var arr = parseSources(s.sources_json);
        var pool = sources.value || [];
        var mine = customs.value || [];
        if (!arr.length) {
          return pool.filter(function (x) { return x.enabled; }).map(function (x) { return x.name; })
            .concat(mine.filter(function (x) { return x.enabled; }).map(function (x) { return x.name; }));
        }
        return arr.map(function (id) {
          if (id.indexOf("cs:") === 0) {
            var cid = Number(id.slice(3));
            var c = mine.filter(function (x) { return x.id === cid; })[0];
            return c ? c.name : (id + "（已删除）");
          }
          var hit = pool.filter(function (x) { return x.id === id; })[0];
          return hit ? hit.name : id;
        });
      }
      function enabledSourceCount() {
        return (sources.value || []).filter(function (x) { return x.enabled; }).length;
      }

      /* -------------------------------------- 自定义源 */
      var customs = ref([]);
      var customOn = ref(true);
      var limits = ref({ max_per_user: 10, max_per_sub: 5 });
      var customModal = ref(false);
      var customEditing = ref(false);
      var customForm = reactive({ id: null, name: "", url: "" });
      var customErr = ref("");

      function loadCustoms() {
        return api("/custom-sources").then(function (d) {
          customs.value = d.sources || [];
          customOn.value = d.enabled !== false;
          if (d.limits) limits.value = d.limits;
        });
      }
      function openCustoms() {
        view.value = "customs";
        loadCustoms().catch(function (e) { toast(e.message, "err"); });
      }
      function resetCustomForm() {
        customForm.id = null; customForm.name = ""; customForm.url = ""; customErr.value = "";
      }
      function openNewCustom() {
        resetCustomForm(); customEditing.value = false; customModal.value = true;
      }
      function openEditCustom(c) {
        resetCustomForm();
        customForm.id = c.id; customForm.name = c.name; customForm.url = c.url;
        customEditing.value = true; customModal.value = true;
      }
      function saveCustom() {
        customErr.value = "";
        var name = (customForm.name || "").trim();
        var url = (customForm.url || "").trim();
        if (!name || !url) { customErr.value = "名称与订阅地址均为必填"; return; }
        if (!/^https?:\/\//i.test(url)) { customErr.value = "地址需以 http:// 或 https:// 开头"; return; }
        var payload = { name: name, url: url };
        busy.value = true;
        var p = customEditing.value
          ? api("/custom-sources/" + customForm.id, { method: "PUT", body: JSON.stringify(payload) })
          : api("/custom-sources", { method: "POST", body: JSON.stringify(payload) });
        p.then(function (d) {
          toast(d.message || (customEditing.value ? "已更新" : "已添加"), "ok");
          customModal.value = false;
          return loadCustoms();
        }).catch(function (e) { customErr.value = e.message; })
          .finally(function () { busy.value = false; });
      }
      function testCustom(c) {
        toast("正在检测「" + c.name + "」…");
        api("/custom-sources/" + c.id + "/test", { method: "POST" })
          .then(function (d) {
            if (d.ok) toast("抓取正常，共 " + d.items + " 条", "ok");
            else toast("抓取失败：" + (d.error || "未知错误"), "err");
            return loadCustoms();
          })
          .catch(function (e) { toast(e.message, "err"); loadCustoms(); });
      }
      function toggleCustom(c) {
        api("/custom-sources/" + c.id, { method: "PUT", body: JSON.stringify({ enabled: !c.enabled }) })
          .then(function () { toast(c.enabled ? "已停用" : "已启用", "ok"); return loadCustoms(); })
          .catch(function (e) { toast(e.message, "err"); });
      }
      function deleteCustom(c) {
        if (!window.confirm("确认删除自定义源「" + c.name + "」？引用它的订阅会被自动移除该源。")) return;
        api("/custom-sources/" + c.id, { method: "DELETE" })
          .then(function () { toast("已删除", "ok"); return Promise.all([loadCustoms(), loadSubs()]); })
          .catch(function (e) { toast(e.message, "err"); });
      }
      function customStatus(c) {
        if (!c.enabled) return { cls: "gray", text: "已停用" };
        if (c.status === "disabled") return { cls: "red", text: "自动禁用" };
        if (c.status === "error") return { cls: "amber", text: "抓取异常" };
        return { cls: "green", text: "正常" };
      }
      function customPill(c) { return customStatus(c).cls; }
      function customStatusText(c) { return customStatus(c).text; }
      var customDisabled = computed(function () { return !customOn.value; });
      function customPill(c) { return customStatus(c).cls; }
      function customStatusText(c) { return customStatus(c).text; }
      var customDisabled = computed(function () { return !customOn.value; });

      /* -------------------------------------- 生命周期 */
      onMounted(function () {
        if (!authed.value) return;
        loadAll().then(function () {
          if (initView === "reader" && initSub) {
            var s = subs.value.filter(function (x) { return String(x.id) === String(initSub); })[0];
            if (s) openReader(s);
          } else if (initView === "subscriptions" || initView === "sources" || initView === "customs") {
            view.value = initView;
          }
        }).catch(function () { doLogout(); });
      });

      return {
        // 基础
        token: token, username: username, authed: authed, view: view, toasts: toasts, busy: busy,
        config: config, sources: sources, subs: subs, dash: dash, toast: toast,
        // 登录
        loginForm: loginForm, loginErr: loginErr, doLogin: doLogin, doLogout: doLogout,
        // 订阅
        subModal: subModal, subEditing: subEditing, subForm: subForm,
        openNewSub: openNewSub, openEditSub: openEditSub, saveSub: saveSub,
        deleteSub: deleteSub, toggleSub: toggleSub, runSub: runSub,
        // 预览
        previewModal: previewModal, previewForm: previewForm, previewMd: previewMd,
        previewStats: previewStats, previewDone: previewDone, previewRendered: previewRendered,
        openPreview: openPreview, doPreview: doPreview,
        // 阅读
        readerSub: readerSub, briefings: briefings, currentBriefing: currentBriefing,
        articles: articles, trend: trend, readerLoading: readerLoading, renderedMd: renderedMd,
        openReader: openReader, selectBriefing: selectBriefing, downloadBriefing: downloadBriefing,
        statValue: statValue, statsOf: statsOf,
        // 自定义源
        customs: customs, customOn: customOn, customDisabled: customDisabled, limits: limits,
        customModal: customModal, customEditing: customEditing, customForm: customForm, customErr: customErr,
        openCustoms: openCustoms, openNewCustom: openNewCustom, openEditCustom: openEditCustom,
        saveCustom: saveCustom, testCustom: testCustom, toggleCustom: toggleCustom,
        deleteCustom: deleteCustom, customStatus: customStatus,
        customPill: customPill, customStatusText: customStatusText, loadCustoms: loadCustoms,
        // 工具
        fmtTime: fmtTime, loadAll: loadAll, catName: catName,
        srcList: srcList, enabledSourceCount: enabledSourceCount,
        maxSeries: computed(function () {
          var m = 1;
          (trend.value.series || []).forEach(function (x) { if (x.article_count > m) m = x.article_count; });
          return m;
        }),
      };
    },
  });

  app.mount("#app");
})();