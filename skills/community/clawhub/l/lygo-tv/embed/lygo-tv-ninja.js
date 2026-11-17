/* LYGO TV Ninja — rooms first (Rumble default), then the public catalog. The catalog endpoint is open to
   read; the public FAST/world lists inside the player UI wait for a per-session Terms tick. Catalog entries
   are remote data and are URL-checked before anything is framed or played (see urlAllowed below). */
(function () {
  "use strict";
  const TV_PAGE = "https://chatagent.ca/sources/";
  const HLS_SRC = "https://cdn.jsdelivr.net/npm/hls.js@1.5.18/dist/hls.min.js";
  // Pinned with Subresource Integrity, so a swapped or tampered copy at the CDN fails to run instead of
  // executing in the visitor's browser. The hash is of the file npm publishes for 1.5.18 (verified against
  // the tarball, not only against the CDN).
  const HLS_SRI = "sha384-R2JqybiEexSXz60H6Zz28MdsqWWnMQlP+NDb7nIhDHWxx6sM7Otw7OWCq9EBCPsz";
  const DEFAULT_ID = "rumble_live";
  const POOL_MAX = 12000;
  const MAX_BYTES = 8000000;
  const EMBED = { youtube: 1, rumble: 1, twitch: 1, kick: 1 };
  const SOUND_KEY = "lygo_tv_sound";
  // Embed kinds are pinned to their own platform's hosts; a stream has to be plain https with no credentials.
  const EMBED_HOSTS = {
    rumble: ["rumble.com", "www.rumble.com"],
    kick: ["player.kick.com", "kick.com", "www.kick.com"],
    twitch: ["player.twitch.tv", "www.twitch.tv", "twitch.tv"],
    youtube: ["www.youtube-nocookie.com", "youtube-nocookie.com", "www.youtube.com", "youtube.com"],
  };

  function kindOf(ch) {
    const k = ch && ch.kind;
    if (k && EMBED[k]) return k;
    const u = String((ch && ch.url) || "").toLowerCase();
    if (u.indexOf("rumble.com") !== -1) return "rumble";
    if (u.indexOf("kick.com") !== -1) return "kick";
    if (u.indexOf("twitch.tv") !== -1) return "twitch";
    if (u.indexOf("youtube") !== -1) return "youtube";
    return "";
  }

  // The only door a catalog URL can come through. Returns the parsed href, or "" for anything refused:
  // not https, carrying credentials, holding control characters, unparseable, or - for an embed kind -
  // pointing at a host that is not that platform's. Exposed so a page can ask the same question.
  function urlAllowed(raw, kind) {
    const s = String(raw == null ? "" : raw).trim();
    if (!s || /[\u0000-\u001f\u007f]/.test(s)) return "";
    let u;
    try { u = new URL(s); } catch (e) { return ""; }
    if (u.protocol !== "https:" || u.username || u.password) return "";
    if (kind && EMBED[kind] && EMBED_HOSTS[kind].indexOf(u.hostname.toLowerCase()) === -1) return "";
    return u.href;
  }
  window.LYGO_TV_ALLOWED_URL = urlAllowed;
  // Every channel used to be silent, on every channel, always: the mute was baked into the embed URL
  // (mute=1 / muted=true) to satisfy the browser's autoplay rule, and nothing ever took it back off.
  // Sound is a preference here ("want") that only applies once a real click has happened in this
  // player ("gesture") - that click is what tells the browser this visitor wants audio.
  let want = false;
  let gesture = false;
  try { want = localStorage.getItem(SOUND_KEY) === "1"; } catch (e) {}
  function mutedNow() { return !(want && gesture); }
  const ROOMS = [
    { id: "rumble_live", title: "Excavationpro Rumble LIVE", kind: "rumble",
      url: "https://rumble.com/embed/v7b5p30/?pub=1th29y", https: true },
    { id: "kick_live", title: "Excavationpro on Kick", kind: "kick",
      url: "https://player.kick.com/excavationpro?autoplay=true", https: true },
    { id: "twitch_live", title: "Excavationpro on Twitch", kind: "twitch",
      channel: "excavationpro", https: true },
    { id: "yt_justin_live", title: "Justin Helmer YouTube LIVE", kind: "youtube",
      url: "https://www.youtube-nocookie.com/embed/live_stream?channel=UCIbGSxMpDaj5ivh6mP_-k-A", https: true },
    { id: "yt_excav_live", title: "Excavationpro YouTube LIVE", kind: "youtube",
      url: "https://www.youtube-nocookie.com/embed/live_stream?channel=UCr2GPEJcl2lXu0lS9-0FjvA", https: true },
    { id: "rumble_radio", title: "Excavationpro Rumble radio", kind: "rumble",
      url: "https://rumble.com/embed/v7anxls/?pub=1th29y", https: true },
    { id: "yt_justin_videos", title: "Justin Helmer YouTube videos", kind: "youtube",
      url: "https://www.youtube-nocookie.com/embed/videoseries?list=UUIbGSxMpDaj5ivh6mP_-k-A", https: true },
    { id: "yt_excav_videos", title: "Excavationpro YouTube videos", kind: "youtube",
      url: "https://www.youtube-nocookie.com/embed/videoseries?list=UUr2GPEJcl2lXu0lS9-0FjvA", https: true }
  ];

  let hlsLib = null;
  let hlsLibLoading = null;

  function loadHls(cb) {
    if (window.Hls) { cb(null); return; }
    if (hlsLibLoading) { hlsLibLoading.push(cb); return; }
    hlsLibLoading = [cb];
    const s = document.createElement("script");
    s.src = HLS_SRC;
    s.integrity = HLS_SRI;
    s.crossOrigin = "anonymous";
    s.async = true;
    s.onload = function () {
      const q = hlsLibLoading || [];
      hlsLibLoading = null;
      q.forEach(function (fn) { fn(null); });
    };
    s.onerror = function () {
      const q = hlsLibLoading || [];
      hlsLibLoading = null;
      q.forEach(function (fn) { fn(new Error("hls")); });
    };
    document.head.appendChild(s);
  }

  function withParam(url, key, val) {
    if (!url) return url;
    try {
      const u = new URL(url);
      u.searchParams.set(key, val);
      return u.toString();
    } catch (e) {
      const join = url.indexOf("?") >= 0 ? "&" : "?";
      return url + join + encodeURIComponent(key) + "=" + encodeURIComponent(val);
    }
  }

  function kindOfUrl(url) {
    const u = String(url || "").toLowerCase().split("?")[0];
    if (u.indexOf("youtube.com") !== -1 || u.indexOf("youtube-nocookie.com") !== -1) return "youtube";
    if (u.indexOf("rumble.com") !== -1) return "rumble";
    if (u.indexOf("twitch.tv") !== -1 || u.indexOf("player.twitch.tv") !== -1) return "twitch";
    if (u.indexOf("kick.com") !== -1 || u.indexOf("player.kick.com") !== -1) return "kick";
    return "hls";
  }

  function isAdult(title, group, bouquetId) {
    const t = String(title || "").toLowerCase();
    const g = String(group || "").toLowerCase();
    const hay = t + " " + g + " " + String(bouquetId || "").toLowerCase();
    if (bouquetId === "mature_18" || bouquetId === "mature" || bouquetId === "xxx") return true;
    if (/^(xxx|adult|18\+|nsfw|porn|porno)$/.test(g)) return true;
    if (/\bxxx\b|\bnsfw\b|\bporn\b|\bporno\b|\bhentai\b|\b18\s*\+/.test(hay)) return true;
    if (/\badult\b/.test(hay) && !/\badult swim\b/.test(hay)) return true;
    return false;
  }

  function embed(ch) {
    if (ch.kind === "twitch" || (ch.url && String(ch.url).indexOf("player.twitch.tv") !== -1)) {
      return "https://player.twitch.tv/?channel=" + encodeURIComponent(ch.channel || "excavationpro") +
        "&parent=" + encodeURIComponent(location.hostname) + "&autoplay=true" +
        (mutedNow() ? "&muted=true" : "");
    }
    let url = ch.url || "";
    if (ch.kind === "rumble" || url.indexOf("rumble.com") !== -1) {
      url = withParam(url, "autoplay", "2");
      return url;
    }
    if (ch.kind === "youtube" || url.indexOf("youtube") !== -1) {
      url = withParam(url, "autoplay", "1");
      url = withParam(url, "mute", mutedNow() ? "1" : "0");
      url = withParam(url, "playsinline", "1");
      return url;
    }
    if (ch.kind === "kick" || url.indexOf("kick.com") !== -1) {
      url = withParam(url, "autoplay", "true");
      url = withParam(url, "muted", mutedNow() ? "true" : "false");
      return url;
    }
    // Rumble takes no mute parameter from outside: it carries its own control inside the frame, and a
    // reload that happens inside a click is what lets the browser give it sound.
    return url;
  }

  function portalHref(ch) {
    if (ch.id && EMBED[ch.kind]) return TV_PAGE + "#channel/" + encodeURIComponent(ch.id);
    if (ch.bouquetId) return TV_PAGE + "#fast/" + encodeURIComponent(ch.bouquetId);
    return TV_PAGE + "#channel/" + DEFAULT_ID;
  }

  function parseM3U(text, bouquetId) {
    const lines = String(text || "").split(/\r?\n/);
    const out = [];
    let title = "";
    let group = "";
    for (let i = 0; i < lines.length; i++) {
      const line = lines[i].trim();
      if (!line) continue;
      if (line.indexOf("#EXTINF") === 0) {
        const comma = line.lastIndexOf(",");
        title = comma >= 0 ? line.slice(comma + 1).trim() : "Channel";
        const gm = line.match(/group-title="([^"]+)"/i);
        group = gm ? gm[1] : "";
        continue;
      }
      if (line.charAt(0) === "#") continue;
      let href = "";
      try { href = new URL(line).href; } catch (e) { title = ""; group = ""; continue; }
      if (href.indexOf("https://") !== 0) { title = ""; group = ""; continue; }
      if (isAdult(title, group, bouquetId)) { title = ""; group = ""; continue; }
      out.push({
        title: title || href,
        url: href,
        https: true,
        kind: kindOfUrl(href),
        group: group,
        bouquetId: bouquetId
      });
      title = "";
      group = "";
      if (out.length >= 3500) break;
    }
    return out;
  }

  function rumbleIndex(list) {
    const i = list.findIndex(function (c) { return c.id === DEFAULT_ID; });
    return i >= 0 ? i : 0;
  }

  function mount(host) {
    if (!host || host.getAttribute("data-lygo-ready")) return;
    host.setAttribute("data-lygo-ready", "1");
    host.classList.add("lygo-tv-ninja");
    host.innerHTML =
      '<div class="tv-top">' +
        '<p class="tv-kicker">LYGO TV</p>' +
        '<a class="tv-open" target="_blank" rel="noopener noreferrer" href="' + TV_PAGE + "#channel/" + DEFAULT_ID + '">Open player</a>' +
      "</div>" +
      '<div class="tv-screen">' +
        '<iframe title="LYGO TV channel" referrerpolicy="no-referrer" allow="autoplay; encrypted-media; fullscreen; picture-in-picture" allowfullscreen></iframe>' +
        '<video playsinline muted autoplay></video>' +
      "</div>" +
      '<div class="tv-bar">' +
        '<button type="button" class="tv-zap" data-dir="-1" aria-label="Previous channel">Prev</button>' +
        '<p class="tv-meta">Channel</p>' +
        '<button type="button" class="tv-zap" data-dir="1" aria-label="Next channel">Next</button>' +
        '<button type="button" class="tv-zap tv-sound" data-sound aria-pressed="false"' +
        ' title="Sound on or off">\uD83D\uDD07 Sound</button>' +
      "</div>" +
      '<p class="tv-meta tv-hint" data-sound-hint hidden style="font-size:.78em;opacity:.78"></p>';

    const list = ROOMS.slice();
    const seen = {};
    list.forEach(function (c) { if (c.url) seen[c.url] = 1; });
    let i = rumbleIndex(list);
    let hls = null;
    const frame = host.querySelector("iframe");
    const video = host.querySelector("video");
    const meta = host.querySelector(".tv-meta");
    const open = host.querySelector(".tv-open");

    function stopHls() {
      if (hls) { try { hls.destroy(); } catch (e) {} hls = null; }
      video.pause();
      video.removeAttribute("src");
      video.load();
    }

    function playHls(url) {
      frame.hidden = true;
      frame.removeAttribute("src");
      video.hidden = false;
      video.muted = mutedNow();
      if (video.canPlayType("application/vnd.apple.mpegurl")) {
        video.src = url;
        video.play().catch(function () {});
        return;
      }
      loadHls(function (err) {
        if (err || !window.Hls || !window.Hls.isSupported()) return;
        stopHls();
        video.hidden = false;
        hls = new window.Hls({ enableWorker: true, xhrSetup: function (xhr) { xhr.withCredentials = false; } });
        hls.loadSource(url);
        hls.attachMedia(video);
        hls.on(window.Hls.Events.MANIFEST_PARSED, function () {
          video.play().catch(function () {});
        });
      });
    }

    function play(n) {
      if (!list.length) return;
      i = (n + list.length) % list.length;
      const ch = list[i];
      const safe = urlAllowed(ch.url, kindOf(ch));
      meta.textContent = ch.title + " · " + (i + 1) + " / " + list.length;
      open.href = portalHref(ch);
      if (!safe) {
        // Belt and braces: merge() already drops these, so arriving here means the pool came from elsewhere.
        // Never hand an unreviewed URL to the frame or the video.
        stopHls();
        video.hidden = true;
        frame.hidden = false;
        frame.removeAttribute("src");
        frame.title = "Channel not loaded";
        hint.textContent = "That channel's source is not an https address on a host this player trusts, so it was not loaded.";
        return;
      }
      if (EMBED[ch.kind]) {
        stopHls();
        video.hidden = true;
        frame.hidden = false;
        frame.setAttribute("allow", "autoplay; encrypted-media; fullscreen; picture-in-picture");
        frame.title = ch.title;
        const src = embed(ch);
        if (frame.getAttribute("src") === src) {
          // Same URL again (the sound toggle reloads the channel so the embed re-reads it). The blank
          // hop is only needed for that case - and it must not depend on requestAnimationFrame, which a
          // backgrounded tab never runs, leaving the screen stuck blank on the channel just asked for.
          frame.src = "about:blank";
          window.setTimeout(function () { frame.src = src; }, 0);
        } else {
          frame.src = src;
        }
        return;
      }
      playHls(ch.url);
    }

    function merge(chs) {
      if (!chs || !chs.length) return;
      for (let n = 0; n < chs.length; n++) {
        const c = chs[n];
        if (!c || !c.url || seen[c.url]) continue;
        if (!urlAllowed(c.url, kindOf(c))) continue;
        seen[c.url] = 1;
        list.push(c);
        if (list.length >= POOL_MAX) break;
      }
      const ch = list[i];
      if (ch) meta.textContent = ch.title + " · " + (i + 1) + " / " + list.length;
    }

    const soundBtn = host.querySelector("[data-sound]");
    const hint = host.querySelector("[data-sound-hint]");
    function paintSound() {
      if (!soundBtn) return;
      soundBtn.textContent = (want ? "\uD83D\uDD0A" : "\uD83D\uDD07") + " Sound";
      soundBtn.setAttribute("aria-pressed", want ? "true" : "false");
      if (hint) {
        const pending = want && !gesture;
        hint.hidden = !pending;
        hint.textContent = pending
          ? "Sound is set to on. The browser needs one click here before it will play audio - press Sound, or Prev/Next."
          : "";
      }
    }
    if (soundBtn) {
      soundBtn.addEventListener("click", function () {
        want = !want;
        gesture = true;                 // a real click: from here the browser allows audio
        try { localStorage.setItem(SOUND_KEY, want ? "1" : "0"); } catch (e) {}
        paintSound();
        play(i);                        // reload the channel under the rule that now applies
      });
    }
    host.querySelectorAll(".tv-zap[data-dir]").forEach(function (btn) {
      btn.addEventListener("click", function () {
        gesture = true;                 // walking channels is a click too: keep the sound decision
        play(i + parseInt(btn.getAttribute("data-dir"), 10));
      });
    });
    paintSound();
    video.hidden = true;
    play(i);
    if (window.IntersectionObserver) {
      const io = new IntersectionObserver(function (ents) {
        if (!ents[0] || !ents[0].isIntersecting) return;
        play(i);
        io.disconnect();
      }, { threshold: 0.2, rootMargin: "120px" });
      io.observe(host);
    }
    window.addEventListener("load", function () { play(i); }, { once: true });

    fetch(TV_PAGE + "catalog.json", { cache: "no-store" }).then(function (r) { return r.json(); }).then(function (cat) {
      if (!cat) return;
      merge((cat.live || []).map(function (ch) {
        ch.https = true;
        ch.kind = ch.kind || kindOfUrl(ch.url);
        return ch;
      }));
      const bouquets = cat.bouquets || [];
      let q = bouquets.slice();
      function one() {
        const b = q.shift();
        if (!b) return;
        if (!b.url || String(b.url).indexOf("https://") !== 0) { one(); return; }
        if (isAdult("", "", b.id)) { one(); return; }
        const ctrl = new AbortController();
        const t = window.setTimeout(function () { ctrl.abort(); }, 14000);
        fetch(b.url, { signal: ctrl.signal, credentials: "omit", cache: "no-store" })
          .then(function (res) { return res.ok ? res.arrayBuffer() : null; })
          .then(function (buf) {
            if (!buf || buf.byteLength > MAX_BYTES) return;
            const text = new TextDecoder("utf-8").decode(buf);
            merge(parseM3U(text, b.id));
          })
          .catch(function () {})
          .then(function () {
            window.clearTimeout(t);
            one();
          });
      }
      one();
      one();
      one();
    }).catch(function () {});
  }

  function boot() {
    document.querySelectorAll("[data-lygo-tv]").forEach(mount);
  }
  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", boot);
  else boot();
})();
