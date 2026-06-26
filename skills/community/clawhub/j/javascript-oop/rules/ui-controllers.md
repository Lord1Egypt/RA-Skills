# UI Controllers

- Treat stateful browser behavior as interface-layer controller classes.
- Accept root elements, documents, selectors, and collaborators through a parameter
  object.
- Keep constructors dependency-only; move DOM queries, event binding, and initial render
  into `start()` or a static factory.
- Keep DOM references, UI state, and cleanup handles in `#private` fields.
- Use intent methods such as `selectTab()`, `advance()`, `open()`, and `render()` instead
  of anonymous inline workflows.
- Make `start()` safe to call once, and provide `destroy()` when listeners or timers need
  cleanup.
- Prefer `AbortController` for listener cleanup in evergreen browsers.
- Remove debug logging, commented-out alternatives, and exercise scaffolding from
  canonical code samples.

## Example

```js
export class TabsController {
    
    #rootElement;
    #tabElements = [];
    #panelElements = [];
    #activeIndex;
    #abortController = null;

    constructor({ rootElement, initialIndex = 0 }) {
        this.#rootElement = rootElement;
        this.#activeIndex = initialIndex;
    }

    start() {
        if (!this.#rootElement || this.#abortController) {
            return;
        }

        this.#tabElements = Array.from(this.#rootElement.querySelectorAll("nav li"));
        this.#panelElements = Array.from(this.#rootElement.querySelectorAll(":scope > article"));
        this.#abortController = new AbortController();

        this.#tabElements.forEach((tabElement, index) => {
            tabElement.addEventListener("click", () => this.#selectTab(index), {
                signal: this.#abortController.signal,
            });
        });

        this.#selectTab(this.#activeIndex);
    }

    destroy() {
        this.#abortController?.abort();
        this.#abortController = null;
    }

    #selectTab(index) {
        this.#activeIndex = index;
        this.#render();
    }

    #render() {
        this.#tabElements.forEach((tabElement, index) => {
            tabElement.classList.toggle("active", index === this.#activeIndex);
        });
        this.#panelElements.forEach((panelElement, index) => {
            panelElement.classList.toggle("hiddenclass", index !== this.#activeIndex);
        });
    }
}
```

## End Check

- Verify the class sits in the `interface` layer and owns only UI state.
- Verify constructors stay dependency-only and `start()` performs binding and initial
  render.
- Verify listener cleanup is explicit when the controller can be torn down.
- Verify DOM behavior is named through intent methods rather than hidden in callbacks.
- Verify canonical samples stay free of debug logs and commented-out legacy code.
