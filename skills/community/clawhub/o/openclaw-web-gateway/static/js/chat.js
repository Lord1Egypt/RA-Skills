(() => {
  function waitForUI(retries = 80) {
    return new Promise((resolve, reject) => {
      function check() {
        if (window.GatewayUI) {
          resolve(window.GatewayUI);
          return;
        }
        if (retries <= 0) {
          reject(new Error("GatewayUI not found"));
          return;
        }
        retries -= 1;
        setTimeout(check, 50);
      }
      check();
    });
  }

  async function init() {
    let ui;
    try {
      ui = await waitForUI();
    } catch (err) {
      console.error(err);
      return;
    }

    const dom = ui.dom;
    const state = ui.state;
    const typingRow = document.getElementById("typingRow");

    function showTyping(flag) {
      if (typingRow) typingRow.style.display = flag ? "flex" : "none";
    }

    async function sendMessage() {
      if (!dom.messageInput) return;
      const text = (dom.messageInput.value || "").trim();
      if (!text || state.thinking) return;

      const userAtSendTime = state.activeUser;
      ui.appendMessage("user", text, userAtSendTime);
      dom.messageInput.value = "";
      ui.autoResizeTextarea();
      ui.setThinking(true);
      showTyping(true);

      try {
        const response = await fetch("/api/chat", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            user: userAtSendTime,
            message: text,
            history: ui.state.histories[userAtSendTime] || [],
          }),
        });

        const data = await response.json().catch(() => ({}));
        if (!response.ok) {
          ui.appendMessage("assistant", data.error || `Server error (${response.status})`, userAtSendTime);
          return;
        }

        ui.appendMessage("assistant", data.reply || "No reply received.", userAtSendTime);

        if (data.action?.type === "open_route") {
          ui.openRoute(data.action.origin || "", data.action.destination || "");
        }
        if (data.action?.type === "open_route_search") {
          ui.openRouteSearch(data.action.query || "");
        }
        if (data.action?.type === "open_web") {
          ui.openWebSearch(data.action.query || "");
        }
        if (data.action?.type === "open_map") {
          ui.openMapSearch(data.action.query || "");
        }
      } catch (err) {
        console.error("Fetch error /api/chat:", err);
        ui.appendMessage("assistant", "Connection error.", userAtSendTime);
      } finally {
        ui.setThinking(false);
        showTyping(false);
        dom.messageInput?.focus();
      }
    }

    dom.sendBtn?.addEventListener("click", (e) => {
      e.preventDefault();
      sendMessage();
    });

    dom.messageInput?.addEventListener("keydown", (e) => {
      if (e.key === "Enter" && !e.shiftKey) {
        e.preventDefault();
        sendMessage();
      }
    });

    dom.messageInput?.addEventListener("focus", () => setTimeout(ui.autoScroll, 150));
    window.addEventListener("load", () => ui.autoScroll());
    window.addEventListener("resize", () => setTimeout(ui.autoScroll, 100));
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init, { once: true });
  } else {
    init();
  }
})();
