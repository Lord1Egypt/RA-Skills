/* Docsify configuration + route guard for the MD Web viewer.
 *
 * This lives in its own file instead of an inline <script> in index.html so the
 * page can run under a Content-Security-Policy that leaves 'unsafe-inline' out
 * of script-src. That is the part that matters: a rendered Markdown document is
 * inserted as HTML, so raw HTML in a document can carry an inline <script>, an
 * onerror= handler or a javascript: URL — all of which need 'unsafe-inline' and
 * are therefore refused by the policy.
 *
 * It also has to load *before* docsify.min.js, so that the guard has already
 * rewritten a hostile location.hash by the time docsify reads the route for the
 * first time. Deployment puts assets in assets/<bundle-hash>/, so old pages
 * keep loading their own bundle while a newer viewer is being provisioned.
 */
(function () {
  "use strict";

  // Every document this skill uploads lives under this key prefix in the bucket.
  var DOC_PREFIX = "/md-web/";

  /* A document route comes from the URL fragment, i.e. from a link that anyone
   * can be sent. Docsify treats a route containing ":" or "//" as a remote URL
   * and fetches it with XMLHttpRequest, and the renderer does not sanitize what
   * comes back — so a CORS-permitting host could otherwise supply the Markdown
   * that renders on this origin. Accept only same-origin paths under md-web/,
   * plus the landing page, and refuse everything else. */
  function isDocRoute(route) {
    var raw = String(route == null ? "" : route).replace(/^#/, "").split("?")[0];
    if (raw === "" || raw === "/" || raw === "/index.html") return true;
    if (raw.charAt(0) !== "/") return false;
    // Any scheme (http:, javascript:, data:) or a protocol-relative //host/path.
    if (/[a-z][a-z0-9+.-]*:/i.test(raw)) return false;
    if (raw.indexOf("//") !== -1) return false;

    var decoded;
    try {
      decoded = decodeURIComponent(raw);
    } catch (e) {
      return false; // malformed percent-encoding
    }
    // Checked again after decoding: %2e%2e/ and %5c only become traversal and a
    // backslash here, and the checks above never saw them.
    if (/[\u0000-\u001f\u007f\\]/.test(decoded)) return false;
    if (decoded.indexOf("//") !== -1) return false;
    if (decoded.split("/").indexOf("..") !== -1) return false;
    return decoded.indexOf(DOC_PREFIX) === 0;
  }

  function landingUrl() {
    return location.pathname + location.search + "#/";
  }

  // First load: correct the hash before docsify parses it. replaceState keeps the
  // crafted URL out of the address bar without adding a history entry.
  if (!isDocRoute(location.hash)) {
    history.replaceState(null, "", landingUrl());
  }

  // Later navigations (a link inside a document, a hand-edited hash) go through
  // the same check. This listener is registered first because config.js loads
  // first, so it runs before docsify's own hashchange handler starts the fetch.
  var indexedRoute = location.hash.replace(/^#/, "").split("?")[0] || "/";
  window.addEventListener("hashchange", function () {
    if (!isDocRoute(location.hash)) {
      location.replace(landingUrl());
      return;
    }
    var nextRoute = location.hash.replace(/^#/, "").split("?")[0] || "/";
    if (nextRoute !== indexedRoute) location.reload();
  });

  window.$docsify = {
    name: "<p>MD Web</p>",
    nameLink: "#/", // relative: also works when public_url has a path prefix
    repo: "https://github.com/rockbenben/aishort-skills/tree/main/skills/md-web",
    notFoundPage: "README.md",
    auto2top: true,

    loadNavbar: false,
    mergeNavbar: true,
    topMargin: 40,

    loadSidebar: false,

    maxLevel: 4,
    subMaxLevel: 2,

    search: {
      // 0, not a day: the index is keyed per path, and md-web serves one document
      // per link. A cached index means the next document a reader opens is searched
      // against the previous one's content and matches nothing. Re-indexing costs one
      // fetch of the single .md being viewed.
      maxAge: 0,
      // Index the document being viewed. "auto" crawls the sidebar, and this server
      // runs with loadSidebar: false — so it only ever indexed the landing README and
      // never the uploaded file, i.e. search matched nothing at all. The hash has
      // already been through isDocRoute() by the time this runs.
      paths: [location.hash.replace(/^#/, "").split("?")[0] || "/"],
      placeholder: "Search",
      noData: "No results found",
      depth: 2,
      hideOtherSidebarContent: false,
    },

    toc: {
      scope: ".markdown-section",
      headings: "h2, h3, h4, h5, h6",
      // Deliberately empty. The bundled table-of-contents plugin writes this
      // string into the page with innerHTML, so any title here would be an HTML
      // sink fed from configuration. Empty leaves the plugin nothing to inject.
      title: "",
    },

    // Name the browser tab after the document, not after this viewer. A link people
    // share ends up in tabs, bookmarks and previews, and "MD Web" told the reader
    // nothing about what they opened. docsify 4 leaves document.title alone, so set
    // it from the first heading and fall back to the static <title>.
    plugins: [
      function (hook) {
        var fallback = document.title;
        hook.doneEach(function () {
          var h = document.querySelector(".markdown-section h1, .markdown-section h2");
          var t = h && h.textContent ? h.textContent.trim() : "";
          document.title = t || fallback;
        });
      },
      function (hook) {
        // Two things the bundled plugins get wrong for a page that renders a
        // document the skill did not write. Both are fixed here, in the file we
        // own, rather than in the vendored builds.
        //
        // 1. The word-count plugin hard-codes language:"english" in its own
        //    defaults, so a Chinese document would get an English counter. The
        //    skill imposes no language on the document — the counter follows
        //    the document's own content, per document, at render time. The
        //    plugin reads the value when it renders, so setting it here is
        //    enough; the range below is the one the plugin itself counts.
        //
        // 2. The table-of-contents plugin writes each entry with innerHTML,
        //    copying the heading's markup into a second place in the page. A
        //    heading in an uploaded document can carry raw HTML, so that copy
        //    turns document markup into live DOM. The entry is reduced to the
        //    inline formatting the sidebar styles expect (span, em, strong,
        //    code, br) with every attribute stripped, so it can only be text.
        var CJK = /[\u4e00-\u9fff]/;
        var TOC_INLINE = { SPAN: 1, EM: 1, STRONG: 1, B: 1, I: 1, CODE: 1, BR: 1, DEL: 1, S: 1 };

        hook.beforeEach(function (markdown) {
          var counter = window.$docsify.count;
          if (counter) {
            counter.language = CJK.test(String(markdown || "")) ? "chinese" : "english";
          }
          return markdown;
        });

        hook.doneEach(function () {
          var entries = document.querySelectorAll(".page_toc a");
          for (var i = 0; i < entries.length; i++) {
            var nodes = entries[i].querySelectorAll("*");
            for (var j = 0; j < nodes.length; j++) {
              var node = nodes[j];
              if (!node.parentNode) continue;
              if (!TOC_INLINE[node.nodeName]) {
                node.parentNode.removeChild(node);
                continue;
              }
              // An inline element may still carry an event handler or a URL
              // that came out of the document; the sidebar only needs the text.
              var attrs = node.attributes;
              for (var k = attrs.length - 1; k >= 0; k--) {
                node.removeAttribute(attrs[k].name);
              }
            }
          }
          // The plugin's title element is filled with innerHTML too. The title
          // above is empty, so this only keeps it that way if a configuration
          // ever changes.
          var title = document.querySelector(".page_toc p.title");
          if (title) title.textContent = title.textContent;
        });
      },
    ],
  };
})();
