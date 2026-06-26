// PageAgent DOM injection script
// Requires page-controller-global.js to be injected first (sets window.PageController)

(function() {
  if (window.__PA__) return 'already_injected';
  if (!window.PageController) return 'error: PageController not found, inject page-controller-global.js first';

  const ctrl = new window.PageController({ viewportExpansion: 0 });

  window.__PA__ = {
    ctrl: ctrl,

    // Get the current page DOM state as LLM-readable text
    async getState() {
      const state = await ctrl.getBrowserState();
      return {
        url: state.url,
        title: state.title,
        header: state.header,
        content: state.content,
        footer: state.footer
      };
    },

    // Click element by index
    async click(index) {
      return await ctrl.clickElement(index);
    },

    // Input text into element by index
    async input(index, text) {
      return await ctrl.inputText(index, text);
    },

    // Select dropdown option
    async select(index, optionText) {
      return await ctrl.selectOption(index, optionText);
    },

    // Scroll
    async scroll(down, pages) {
      return await ctrl.scroll({ down: down !== false, numPages: pages || 1 });
    },

    // Scroll specific element
    async scrollElement(index, down, pages) {
      return await ctrl.scroll({ down: down !== false, numPages: pages || 1, index });
    },

    // Execute JS
    async execJS(script) {
      return await ctrl.executeJavascript(script);
    },

    // Clean up highlights
    async cleanUp() {
      await ctrl.cleanUpHighlights();
    }
  };

  return 'injected';
})();
