var __defProp = Object.defineProperty;
var __name = (target, value) => __defProp(target, "name", { value, configurable: true });
async function waitFor(seconds) {
  await new Promise((resolve) => setTimeout(resolve, seconds * 1e3));
}
__name(waitFor, "waitFor");
async function movePointerToElement(element) {
  const rect = element.getBoundingClientRect();
  const x = rect.left + rect.width / 2;
  const y = rect.top + rect.height / 2;
  window.dispatchEvent(new CustomEvent("PageAgent::MovePointerTo", { detail: { x, y } }));
  await waitFor(0.3);
}
__name(movePointerToElement, "movePointerToElement");
function getElementByIndex(selectorMap, index) {
  const interactiveNode = selectorMap.get(index);
  if (!interactiveNode) {
    throw new Error(`No interactive element found at index ${index}`);
  }
  const element = interactiveNode.ref;
  if (!element) {
    throw new Error(`Element at index ${index} does not have a reference`);
  }
  if (!(element instanceof HTMLElement)) {
    throw new Error(`Element at index ${index} is not an HTMLElement`);
  }
  return element;
}
__name(getElementByIndex, "getElementByIndex");
let lastClickedElement = null;
function blurLastClickedElement() {
  if (lastClickedElement) {
    lastClickedElement.blur();
    lastClickedElement.dispatchEvent(
      new MouseEvent("mouseout", { bubbles: true, cancelable: true })
    );
    lastClickedElement = null;
  }
}
__name(blurLastClickedElement, "blurLastClickedElement");
async function clickElement(element) {
  blurLastClickedElement();
  lastClickedElement = element;
  await scrollIntoViewIfNeeded(element);
  await movePointerToElement(element);
  window.dispatchEvent(new CustomEvent("PageAgent::ClickPointer"));
  await waitFor(0.1);
  element.dispatchEvent(new MouseEvent("mouseenter", { bubbles: true, cancelable: true }));
  element.dispatchEvent(new MouseEvent("mouseover", { bubbles: true, cancelable: true }));
  element.dispatchEvent(new MouseEvent("mousedown", { bubbles: true, cancelable: true }));
  element.focus();
  element.dispatchEvent(new MouseEvent("mouseup", { bubbles: true, cancelable: true }));
  element.dispatchEvent(new MouseEvent("click", { bubbles: true, cancelable: true }));
  await waitFor(0.2);
}
__name(clickElement, "clickElement");
const nativeInputValueSetter = Object.getOwnPropertyDescriptor(
  window.HTMLInputElement.prototype,
  "value"
).set;
const nativeTextAreaValueSetter = Object.getOwnPropertyDescriptor(
  window.HTMLTextAreaElement.prototype,
  "value"
).set;
async function inputTextElement(element, text) {
  const isContentEditable = element.isContentEditable;
  if (!(element instanceof HTMLInputElement) && !(element instanceof HTMLTextAreaElement) && !isContentEditable) {
    throw new Error("Element is not an input, textarea, or contenteditable");
  }
  await clickElement(element);
  if (isContentEditable) {
    if (element.dispatchEvent(
      new InputEvent("beforeinput", {
        bubbles: true,
        cancelable: true,
        inputType: "deleteContent"
      })
    )) {
      element.innerText = "";
      element.dispatchEvent(
        new InputEvent("input", {
          bubbles: true,
          inputType: "deleteContent"
        })
      );
    }
    if (element.dispatchEvent(
      new InputEvent("beforeinput", {
        bubbles: true,
        cancelable: true,
        inputType: "insertText",
        data: text
      })
    )) {
      element.innerText = text;
      element.dispatchEvent(
        new InputEvent("input", {
          bubbles: true,
          inputType: "insertText",
          data: text
        })
      );
    }
    element.dispatchEvent(new Event("change", { bubbles: true }));
    element.blur();
  } else if (element instanceof HTMLTextAreaElement) {
    nativeTextAreaValueSetter.call(element, text);
  } else {
    nativeInputValueSetter.call(element, text);
  }
  if (!isContentEditable) {
    element.dispatchEvent(new Event("input", { bubbles: true }));
  }
  await waitFor(0.1);
  blurLastClickedElement();
}
__name(inputTextElement, "inputTextElement");
async function selectOptionElement(selectElement, optionText) {
  if (!(selectElement instanceof HTMLSelectElement)) {
    throw new Error("Element is not a select element");
  }
  const options = Array.from(selectElement.options);
  const option = options.find((opt) => opt.textContent?.trim() === optionText.trim());
  if (!option) {
    throw new Error(`Option with text "${optionText}" not found in select element`);
  }
  selectElement.value = option.value;
  selectElement.dispatchEvent(new Event("change", { bubbles: true }));
  await waitFor(0.1);
}
__name(selectOptionElement, "selectOptionElement");
async function scrollIntoViewIfNeeded(element) {
  const el = element;
  if (el.scrollIntoViewIfNeeded) {
    el.scrollIntoViewIfNeeded();
  } else {
    el.scrollIntoView({ behavior: "auto", block: "center", inline: "nearest" });
  }
}
__name(scrollIntoViewIfNeeded, "scrollIntoViewIfNeeded");
async function scrollVertically(down, scroll_amount, element) {
  if (element) {
    const targetElement = element;
    let currentElement = targetElement;
    let scrollSuccess = false;
    let scrolledElement = null;
    let scrollDelta = 0;
    let attempts = 0;
    const dy2 = scroll_amount;
    while (currentElement && attempts < 10) {
      const computedStyle = window.getComputedStyle(currentElement);
      const hasScrollableY = /(auto|scroll|overlay)/.test(computedStyle.overflowY);
      const canScrollVertically = currentElement.scrollHeight > currentElement.clientHeight;
      if (hasScrollableY && canScrollVertically) {
        const beforeScroll = currentElement.scrollTop;
        const maxScroll = currentElement.scrollHeight - currentElement.clientHeight;
        let scrollAmount = dy2 / 3;
        if (scrollAmount > 0) {
          scrollAmount = Math.min(scrollAmount, maxScroll - beforeScroll);
        } else {
          scrollAmount = Math.max(scrollAmount, -beforeScroll);
        }
        currentElement.scrollTop = beforeScroll + scrollAmount;
        const afterScroll = currentElement.scrollTop;
        const actualScrollDelta = afterScroll - beforeScroll;
        if (Math.abs(actualScrollDelta) > 0.5) {
          scrollSuccess = true;
          scrolledElement = currentElement;
          scrollDelta = actualScrollDelta;
          break;
        }
      }
      if (currentElement === document.body || currentElement === document.documentElement) {
        break;
      }
      currentElement = currentElement.parentElement;
      attempts++;
    }
    if (scrollSuccess) {
      return `Scrolled container (${scrolledElement?.tagName}) by ${scrollDelta}px`;
    } else {
      return `No scrollable container found for element (${targetElement.tagName})`;
    }
  }
  const dy = scroll_amount;
  const bigEnough = /* @__PURE__ */ __name((el2) => el2.clientHeight >= window.innerHeight * 0.5, "bigEnough");
  const canScroll = /* @__PURE__ */ __name((el2) => el2 && /(auto|scroll|overlay)/.test(getComputedStyle(el2).overflowY) && el2.scrollHeight > el2.clientHeight && bigEnough(el2), "canScroll");
  let el = document.activeElement;
  while (el && !canScroll(el) && el !== document.body) el = el.parentElement;
  el = canScroll(el) ? el : Array.from(document.querySelectorAll("*")).find(canScroll) || document.scrollingElement || document.documentElement;
  if (el === document.scrollingElement || el === document.documentElement || el === document.body) {
    const scrollBefore = window.scrollY;
    const scrollMax = document.documentElement.scrollHeight - window.innerHeight;
    window.scrollBy(0, dy);
    const scrollAfter = window.scrollY;
    const scrolled = scrollAfter - scrollBefore;
    if (Math.abs(scrolled) < 1) {
      return dy > 0 ? `⚠️ Already at the bottom of the page, cannot scroll down further.` : `⚠️ Already at the top of the page, cannot scroll up further.`;
    }
    const reachedBottom = dy > 0 && scrollAfter >= scrollMax - 1;
    const reachedTop = dy < 0 && scrollAfter <= 1;
    if (reachedBottom) return `✅ Scrolled page by ${scrolled}px. Reached the bottom of the page.`;
    if (reachedTop) return `✅ Scrolled page by ${scrolled}px. Reached the top of the page.`;
    return `✅ Scrolled page by ${scrolled}px.`;
  } else {
    const scrollBefore = el.scrollTop;
    const scrollMax = el.scrollHeight - el.clientHeight;
    el.scrollBy({ top: dy, behavior: "smooth" });
    await waitFor(0.1);
    const scrollAfter = el.scrollTop;
    const scrolled = scrollAfter - scrollBefore;
    if (Math.abs(scrolled) < 1) {
      return dy > 0 ? `⚠️ Already at the bottom of container (${el.tagName}), cannot scroll down further.` : `⚠️ Already at the top of container (${el.tagName}), cannot scroll up further.`;
    }
    const reachedBottom = dy > 0 && scrollAfter >= scrollMax - 1;
    const reachedTop = dy < 0 && scrollAfter <= 1;
    if (reachedBottom)
      return `✅ Scrolled container (${el.tagName}) by ${scrolled}px. Reached the bottom.`;
    if (reachedTop)
      return `✅ Scrolled container (${el.tagName}) by ${scrolled}px. Reached the top.`;
    return `✅ Scrolled container (${el.tagName}) by ${scrolled}px.`;
  }
}
__name(scrollVertically, "scrollVertically");
async function scrollHorizontally(right, scroll_amount, element) {
  if (element) {
    const targetElement = element;
    let currentElement = targetElement;
    let scrollSuccess = false;
    let scrolledElement = null;
    let scrollDelta = 0;
    let attempts = 0;
    const dx2 = right ? scroll_amount : -scroll_amount;
    while (currentElement && attempts < 10) {
      const computedStyle = window.getComputedStyle(currentElement);
      const hasScrollableX = /(auto|scroll|overlay)/.test(computedStyle.overflowX);
      const canScrollHorizontally = currentElement.scrollWidth > currentElement.clientWidth;
      if (hasScrollableX && canScrollHorizontally) {
        const beforeScroll = currentElement.scrollLeft;
        const maxScroll = currentElement.scrollWidth - currentElement.clientWidth;
        let scrollAmount = dx2 / 3;
        if (scrollAmount > 0) {
          scrollAmount = Math.min(scrollAmount, maxScroll - beforeScroll);
        } else {
          scrollAmount = Math.max(scrollAmount, -beforeScroll);
        }
        currentElement.scrollLeft = beforeScroll + scrollAmount;
        const afterScroll = currentElement.scrollLeft;
        const actualScrollDelta = afterScroll - beforeScroll;
        if (Math.abs(actualScrollDelta) > 0.5) {
          scrollSuccess = true;
          scrolledElement = currentElement;
          scrollDelta = actualScrollDelta;
          break;
        }
      }
      if (currentElement === document.body || currentElement === document.documentElement) {
        break;
      }
      currentElement = currentElement.parentElement;
      attempts++;
    }
    if (scrollSuccess) {
      return `Scrolled container (${scrolledElement?.tagName}) horizontally by ${scrollDelta}px`;
    } else {
      return `No horizontally scrollable container found for element (${targetElement.tagName})`;
    }
  }
  const dx = right ? scroll_amount : -scroll_amount;
  const bigEnough = /* @__PURE__ */ __name((el2) => el2.clientWidth >= window.innerWidth * 0.5, "bigEnough");
  const canScroll = /* @__PURE__ */ __name((el2) => el2 && /(auto|scroll|overlay)/.test(getComputedStyle(el2).overflowX) && el2.scrollWidth > el2.clientWidth && bigEnough(el2), "canScroll");
  let el = document.activeElement;
  while (el && !canScroll(el) && el !== document.body) el = el.parentElement;
  el = canScroll(el) ? el : Array.from(document.querySelectorAll("*")).find(canScroll) || document.scrollingElement || document.documentElement;
  if (el === document.scrollingElement || el === document.documentElement || el === document.body) {
    const scrollBefore = window.scrollX;
    const scrollMax = document.documentElement.scrollWidth - window.innerWidth;
    window.scrollBy(dx, 0);
    const scrollAfter = window.scrollX;
    const scrolled = scrollAfter - scrollBefore;
    if (Math.abs(scrolled) < 1) {
      return dx > 0 ? `⚠️ Already at the right edge of the page, cannot scroll right further.` : `⚠️ Already at the left edge of the page, cannot scroll left further.`;
    }
    const reachedRight = dx > 0 && scrollAfter >= scrollMax - 1;
    const reachedLeft = dx < 0 && scrollAfter <= 1;
    if (reachedRight)
      return `✅ Scrolled page by ${scrolled}px. Reached the right edge of the page.`;
    if (reachedLeft) return `✅ Scrolled page by ${scrolled}px. Reached the left edge of the page.`;
    return `✅ Scrolled page horizontally by ${scrolled}px.`;
  } else {
    const scrollBefore = el.scrollLeft;
    const scrollMax = el.scrollWidth - el.clientWidth;
    el.scrollBy({ left: dx, behavior: "smooth" });
    await waitFor(0.1);
    const scrollAfter = el.scrollLeft;
    const scrolled = scrollAfter - scrollBefore;
    if (Math.abs(scrolled) < 1) {
      return dx > 0 ? `⚠️ Already at the right edge of container (${el.tagName}), cannot scroll right further.` : `⚠️ Already at the left edge of container (${el.tagName}), cannot scroll left further.`;
    }
    const reachedRight = dx > 0 && scrollAfter >= scrollMax - 1;
    const reachedLeft = dx < 0 && scrollAfter <= 1;
    if (reachedRight)
      return `✅ Scrolled container (${el.tagName}) by ${scrolled}px. Reached the right edge.`;
    if (reachedLeft)
      return `✅ Scrolled container (${el.tagName}) by ${scrolled}px. Reached the left edge.`;
    return `✅ Scrolled container (${el.tagName}) horizontally by ${scrolled}px.`;
  }
}
__name(scrollHorizontally, "scrollHorizontally");
const domTree = /* @__PURE__ */ __name((args = {
  doHighlightElements: true,
  focusHighlightIndex: -1,
  viewportExpansion: 0,
  debugMode: false,
  /**
   * @edit
   */
  /** @type {Element[]} */
  interactiveBlacklist: [],
  /** @type {Element[]} */
  interactiveWhitelist: [],
  highlightOpacity: 0.1,
  highlightLabelOpacity: 0.5
}) => {
  const { interactiveBlacklist, interactiveWhitelist, highlightOpacity, highlightLabelOpacity } = args;
  const { doHighlightElements, focusHighlightIndex, viewportExpansion, debugMode } = args;
  let highlightIndex = 0;
  const extraData = /* @__PURE__ */ new WeakMap();
  function addExtraData(element, data) {
    if (!element || element.nodeType !== Node.ELEMENT_NODE) return;
    extraData.set(element, { ...extraData.get(element), ...data });
  }
  __name(addExtraData, "addExtraData");
  const DOM_CACHE = {
    boundingRects: /* @__PURE__ */ new WeakMap(),
    clientRects: /* @__PURE__ */ new WeakMap(),
    computedStyles: /* @__PURE__ */ new WeakMap(),
    clearCache: /* @__PURE__ */ __name(() => {
      DOM_CACHE.boundingRects = /* @__PURE__ */ new WeakMap();
      DOM_CACHE.clientRects = /* @__PURE__ */ new WeakMap();
      DOM_CACHE.computedStyles = /* @__PURE__ */ new WeakMap();
    }, "clearCache")
  };
  function getCachedBoundingRect(element) {
    if (!element) return null;
    if (DOM_CACHE.boundingRects.has(element)) {
      return DOM_CACHE.boundingRects.get(element);
    }
    const rect = element.getBoundingClientRect();
    if (rect) {
      DOM_CACHE.boundingRects.set(element, rect);
    }
    return rect;
  }
  __name(getCachedBoundingRect, "getCachedBoundingRect");
  function getCachedComputedStyle(element) {
    if (!element) return null;
    if (DOM_CACHE.computedStyles.has(element)) {
      return DOM_CACHE.computedStyles.get(element);
    }
    const style = window.getComputedStyle(element);
    if (style) {
      DOM_CACHE.computedStyles.set(element, style);
    }
    return style;
  }
  __name(getCachedComputedStyle, "getCachedComputedStyle");
  function getCachedClientRects(element) {
    if (!element) return null;
    if (DOM_CACHE.clientRects.has(element)) {
      return DOM_CACHE.clientRects.get(element);
    }
    const rects = element.getClientRects();
    if (rects) {
      DOM_CACHE.clientRects.set(element, rects);
    }
    return rects;
  }
  __name(getCachedClientRects, "getCachedClientRects");
  const DOM_HASH_MAP = {};
  const ID = { current: 0 };
  const HIGHLIGHT_CONTAINER_ID = "playwright-highlight-container";
  function highlightElement(element, index, parentIframe = null) {
    if (!element) return index;
    const overlays = [];
    let label = null;
    let labelWidth = 20;
    let labelHeight = 16;
    let cleanupFn = null;
    try {
      let container = document.getElementById(HIGHLIGHT_CONTAINER_ID);
      if (!container) {
        container = document.createElement("div");
        container.id = HIGHLIGHT_CONTAINER_ID;
        container.style.position = "fixed";
        container.style.pointerEvents = "none";
        container.style.top = "0";
        container.style.left = "0";
        container.style.width = "100%";
        container.style.height = "100%";
        container.style.zIndex = "2147483640";
        container.style.backgroundColor = "transparent";
        document.body.appendChild(container);
      }
      const rects = element.getClientRects();
      if (!rects || rects.length === 0) return index;
      const colors = [
        "#FF0000",
        "#00FF00",
        "#0000FF",
        "#FFA500",
        "#800080",
        "#008080",
        "#FF69B4",
        "#4B0082",
        "#FF4500",
        "#2E8B57",
        "#DC143C",
        "#4682B4"
      ];
      const colorIndex = index % colors.length;
      let baseColor = colors[colorIndex];
      const backgroundColor = baseColor + Math.floor(highlightOpacity * 255).toString(16).padStart(2, "0");
      baseColor = baseColor + Math.floor(highlightLabelOpacity * 255).toString(16).padStart(2, "0");
      let iframeOffset = { x: 0, y: 0 };
      if (parentIframe) {
        const iframeRect = parentIframe.getBoundingClientRect();
        iframeOffset.x = iframeRect.left;
        iframeOffset.y = iframeRect.top;
      }
      const fragment = document.createDocumentFragment();
      for (const rect of rects) {
        if (rect.width === 0 || rect.height === 0) continue;
        const overlay = document.createElement("div");
        overlay.style.position = "fixed";
        overlay.style.border = `2px solid ${baseColor}`;
        overlay.style.backgroundColor = backgroundColor;
        overlay.style.pointerEvents = "none";
        overlay.style.boxSizing = "border-box";
        const top = rect.top + iframeOffset.y;
        const left = rect.left + iframeOffset.x;
        overlay.style.top = `${top}px`;
        overlay.style.left = `${left}px`;
        overlay.style.width = `${rect.width}px`;
        overlay.style.height = `${rect.height}px`;
        fragment.appendChild(overlay);
        overlays.push({ element: overlay, initialRect: rect });
      }
      const firstRect = rects[0];
      label = document.createElement("div");
      label.className = "playwright-highlight-label";
      label.style.position = "fixed";
      label.style.background = baseColor;
      label.style.color = "white";
      label.style.padding = "1px 4px";
      label.style.borderRadius = "4px";
      label.style.fontSize = `${Math.min(12, Math.max(8, firstRect.height / 2))}px`;
      label.textContent = index.toString();
      labelWidth = label.offsetWidth > 0 ? label.offsetWidth : labelWidth;
      labelHeight = label.offsetHeight > 0 ? label.offsetHeight : labelHeight;
      const firstRectTop = firstRect.top + iframeOffset.y;
      const firstRectLeft = firstRect.left + iframeOffset.x;
      let labelTop = firstRectTop + 2;
      let labelLeft = firstRectLeft + firstRect.width - labelWidth - 2;
      if (firstRect.width < labelWidth + 4 || firstRect.height < labelHeight + 4) {
        labelTop = firstRectTop - labelHeight - 2;
        labelLeft = firstRectLeft + firstRect.width - labelWidth;
        if (labelLeft < iframeOffset.x) labelLeft = firstRectLeft;
      }
      labelTop = Math.max(0, Math.min(labelTop, window.innerHeight - labelHeight));
      labelLeft = Math.max(0, Math.min(labelLeft, window.innerWidth - labelWidth));
      label.style.top = `${labelTop}px`;
      label.style.left = `${labelLeft}px`;
      fragment.appendChild(label);
      const updatePositions = /* @__PURE__ */ __name(() => {
        const newRects = element.getClientRects();
        let newIframeOffset = { x: 0, y: 0 };
        if (parentIframe) {
          const iframeRect = parentIframe.getBoundingClientRect();
          newIframeOffset.x = iframeRect.left;
          newIframeOffset.y = iframeRect.top;
        }
        overlays.forEach((overlayData, i) => {
          if (i < newRects.length) {
            const newRect = newRects[i];
            const newTop = newRect.top + newIframeOffset.y;
            const newLeft = newRect.left + newIframeOffset.x;
            overlayData.element.style.top = `${newTop}px`;
            overlayData.element.style.left = `${newLeft}px`;
            overlayData.element.style.width = `${newRect.width}px`;
            overlayData.element.style.height = `${newRect.height}px`;
            overlayData.element.style.display = newRect.width === 0 || newRect.height === 0 ? "none" : "block";
          } else {
            overlayData.element.style.display = "none";
          }
        });
        if (newRects.length < overlays.length) {
          for (let i = newRects.length; i < overlays.length; i++) {
            overlays[i].element.style.display = "none";
          }
        }
        if (label && newRects.length > 0) {
          const firstNewRect = newRects[0];
          const firstNewRectTop = firstNewRect.top + newIframeOffset.y;
          const firstNewRectLeft = firstNewRect.left + newIframeOffset.x;
          let newLabelTop = firstNewRectTop + 2;
          let newLabelLeft = firstNewRectLeft + firstNewRect.width - labelWidth - 2;
          if (firstNewRect.width < labelWidth + 4 || firstNewRect.height < labelHeight + 4) {
            newLabelTop = firstNewRectTop - labelHeight - 2;
            newLabelLeft = firstNewRectLeft + firstNewRect.width - labelWidth;
            if (newLabelLeft < newIframeOffset.x) newLabelLeft = firstNewRectLeft;
          }
          newLabelTop = Math.max(0, Math.min(newLabelTop, window.innerHeight - labelHeight));
          newLabelLeft = Math.max(0, Math.min(newLabelLeft, window.innerWidth - labelWidth));
          label.style.top = `${newLabelTop}px`;
          label.style.left = `${newLabelLeft}px`;
          label.style.display = "block";
        } else if (label) {
          label.style.display = "none";
        }
      }, "updatePositions");
      const throttleFunction = /* @__PURE__ */ __name((func, delay) => {
        let lastCall = 0;
        return (...args2) => {
          const now = performance.now();
          if (now - lastCall < delay) return;
          lastCall = now;
          return func(...args2);
        };
      }, "throttleFunction");
      const throttledUpdatePositions = throttleFunction(updatePositions, 16);
      window.addEventListener("scroll", throttledUpdatePositions, true);
      window.addEventListener("resize", throttledUpdatePositions);
      cleanupFn = /* @__PURE__ */ __name(() => {
        window.removeEventListener("scroll", throttledUpdatePositions, true);
        window.removeEventListener("resize", throttledUpdatePositions);
        overlays.forEach((overlay) => overlay.element.remove());
        if (label) label.remove();
      }, "cleanupFn");
      container.appendChild(fragment);
      return index + 1;
    } finally {
      if (cleanupFn) {
        (window._highlightCleanupFunctions = window._highlightCleanupFunctions || []).push(
          cleanupFn
        );
      }
    }
  }
  __name(highlightElement, "highlightElement");
  function isScrollableElement(element) {
    if (!element || element.nodeType !== Node.ELEMENT_NODE) {
      return null;
    }
    const style = getCachedComputedStyle(element);
    if (!style) return null;
    const display = style.display;
    if (display === "inline" || display === "inline-block") {
      return null;
    }
    const overflowX = style.overflowX;
    const overflowY = style.overflowY;
    const scrollableX = overflowX === "auto" || overflowX === "scroll";
    const scrollableY = overflowY === "auto" || overflowY === "scroll";
    if (!scrollableX && !scrollableY) {
      return null;
    }
    const scrollWidth = element.scrollWidth - element.clientWidth;
    const scrollHeight = element.scrollHeight - element.clientHeight;
    const threshold = 4;
    if (scrollWidth < threshold && scrollHeight < threshold) {
      return null;
    }
    if (!scrollableY && scrollWidth < threshold) {
      return null;
    }
    if (!scrollableX && scrollHeight < threshold) {
      return null;
    }
    const distanceToTop = element.scrollTop;
    const distanceToLeft = element.scrollLeft;
    const distanceToRight = element.scrollWidth - element.clientWidth - element.scrollLeft;
    const distanceToBottom = element.scrollHeight - element.clientHeight - element.scrollTop;
    const scrollData = {
      top: distanceToTop,
      right: distanceToRight,
      bottom: distanceToBottom,
      left: distanceToLeft
    };
    addExtraData(element, {
      scrollable: true,
      scrollData
    });
    return scrollData;
  }
  __name(isScrollableElement, "isScrollableElement");
  function isTextNodeVisible(textNode) {
    try {
      if (viewportExpansion === -1) {
        const parentElement2 = textNode.parentElement;
        if (!parentElement2) return false;
        try {
          return parentElement2.checkVisibility({
            checkOpacity: true,
            checkVisibilityCSS: true
          });
        } catch (e) {
          const style = window.getComputedStyle(parentElement2);
          return style.display !== "none" && style.visibility !== "hidden" && style.opacity !== "0";
        }
      }
      const range = document.createRange();
      range.selectNodeContents(textNode);
      const rects = range.getClientRects();
      if (!rects || rects.length === 0) {
        return false;
      }
      let isAnyRectVisible = false;
      let isAnyRectInViewport = false;
      for (const rect of rects) {
        if (rect.width > 0 && rect.height > 0) {
          isAnyRectVisible = true;
          if (!(rect.bottom < -viewportExpansion || rect.top > window.innerHeight + viewportExpansion || rect.right < -viewportExpansion || rect.left > window.innerWidth + viewportExpansion)) {
            isAnyRectInViewport = true;
            break;
          }
        }
      }
      if (!isAnyRectVisible || !isAnyRectInViewport) {
        return false;
      }
      const parentElement = textNode.parentElement;
      if (!parentElement) return false;
      try {
        return parentElement.checkVisibility({
          checkOpacity: true,
          checkVisibilityCSS: true
        });
      } catch (e) {
        const style = window.getComputedStyle(parentElement);
        return style.display !== "none" && style.visibility !== "hidden" && style.opacity !== "0";
      }
    } catch (e) {
      console.warn("Error checking text node visibility:", e);
      return false;
    }
  }
  __name(isTextNodeVisible, "isTextNodeVisible");
  function isElementAccepted(element) {
    if (!element || !element.tagName) return false;
    const alwaysAccept = /* @__PURE__ */ new Set([
      "body",
      "div",
      "main",
      "article",
      "section",
      "nav",
      "header",
      "footer"
    ]);
    const tagName = element.tagName.toLowerCase();
    if (alwaysAccept.has(tagName)) return true;
    const leafElementDenyList = /* @__PURE__ */ new Set([
      "svg",
      "script",
      "style",
      "link",
      "meta",
      "noscript",
      "template"
    ]);
    return !leafElementDenyList.has(tagName);
  }
  __name(isElementAccepted, "isElementAccepted");
  function isElementVisible(element) {
    const style = getCachedComputedStyle(element);
    return element.offsetWidth > 0 && element.offsetHeight > 0 && style?.visibility !== "hidden" && style?.display !== "none";
  }
  __name(isElementVisible, "isElementVisible");
  function isInteractiveElement(element) {
    if (!element || element.nodeType !== Node.ELEMENT_NODE) {
      return false;
    }
    if (interactiveBlacklist.includes(element)) {
      return false;
    }
    if (interactiveWhitelist.includes(element)) {
      return true;
    }
    const tagName = element.tagName.toLowerCase();
    const style = getCachedComputedStyle(element);
    const interactiveCursors = /* @__PURE__ */ new Set([
      "pointer",
      // Link/clickable elements
      "move",
      // Movable elements
      "text",
      // Text selection
      "grab",
      // Grabbable elements
      "grabbing",
      // Currently grabbing
      "cell",
      // Table cell selection
      "copy",
      // Copy operation
      "alias",
      // Alias creation
      "all-scroll",
      // Scrollable content
      "col-resize",
      // Column resize
      "context-menu",
      // Context menu available
      "crosshair",
      // Precise selection
      "e-resize",
      // East resize
      "ew-resize",
      // East-west resize
      "help",
      // Help available
      "n-resize",
      // North resize
      "ne-resize",
      // Northeast resize
      "nesw-resize",
      // Northeast-southwest resize
      "ns-resize",
      // North-south resize
      "nw-resize",
      // Northwest resize
      "nwse-resize",
      // Northwest-southeast resize
      "row-resize",
      // Row resize
      "s-resize",
      // South resize
      "se-resize",
      // Southeast resize
      "sw-resize",
      // Southwest resize
      "vertical-text",
      // Vertical text selection
      "w-resize",
      // West resize
      "zoom-in",
      // Zoom in
      "zoom-out"
      // Zoom out
    ]);
    const nonInteractiveCursors = /* @__PURE__ */ new Set([
      "not-allowed",
      // Action not allowed
      "no-drop",
      // Drop not allowed
      "wait",
      // Processing
      "progress",
      // In progress
      "initial",
      // Initial value
      "inherit"
      // Inherited value
      //? Let's just include all potentially clickable elements that are not specifically blocked
      // 'none',        // No cursor
      // 'default',     // Default cursor
      // 'auto',        // Browser default
    ]);
    function doesElementHaveInteractivePointer(element2) {
      if (element2.tagName.toLowerCase() === "html") return false;
      if (style?.cursor && interactiveCursors.has(style.cursor)) return true;
      return false;
    }
    __name(doesElementHaveInteractivePointer, "doesElementHaveInteractivePointer");
    let isInteractiveCursor = doesElementHaveInteractivePointer(element);
    if (isInteractiveCursor) {
      return true;
    }
    const interactiveElements = /* @__PURE__ */ new Set([
      "a",
      // Links
      "button",
      // Buttons
      "input",
      // All input types (text, checkbox, radio, etc.)
      "select",
      // Dropdown menus
      "textarea",
      // Text areas
      "details",
      // Expandable details
      "summary",
      // Summary element (clickable part of details)
      "label",
      // Form labels (often clickable)
      "option",
      // Select options
      "optgroup",
      // Option groups
      "fieldset",
      // Form fieldsets (can be interactive with legend)
      "legend"
      // Fieldset legends
    ]);
    const explicitDisableTags = /* @__PURE__ */ new Set([
      "disabled",
      // Standard disabled attribute
      // 'aria-disabled',      // ARIA disabled state
      "readonly"
      // Read-only state
      // 'aria-readonly',     // ARIA read-only state
      // 'aria-hidden',       // Hidden from accessibility
      // 'hidden',            // Hidden attribute
      // 'inert',             // Inert attribute
      // 'aria-inert',        // ARIA inert state
      // 'tabindex="-1"',     // Removed from tab order
      // 'aria-hidden="true"' // Hidden from screen readers
    ]);
    if (interactiveElements.has(tagName)) {
      if (style?.cursor && nonInteractiveCursors.has(style.cursor)) {
        return false;
      }
      for (const disableTag of explicitDisableTags) {
        if (element.hasAttribute(disableTag) || element.getAttribute(disableTag) === "true" || element.getAttribute(disableTag) === "") {
          return false;
        }
      }
      if (element.disabled) {
        return false;
      }
      if (element.readOnly) {
        return false;
      }
      if (element.inert) {
        return false;
      }
      return true;
    }
    const role = element.getAttribute("role");
    const ariaRole = element.getAttribute("aria-role");
    if (element.getAttribute("contenteditable") === "true" || element.isContentEditable) {
      return true;
    }
    if (element.classList && (element.classList.contains("button") || element.classList.contains("dropdown-toggle") || element.getAttribute("data-index") || element.getAttribute("data-toggle") === "dropdown" || element.getAttribute("aria-haspopup") === "true")) {
      return true;
    }
    const interactiveRoles = /* @__PURE__ */ new Set([
      "button",
      // Directly clickable element
      // 'link',            // Clickable link
      "menu",
      // Menu container (ARIA menus)
      "menubar",
      // Menu bar container
      "menuitem",
      // Clickable menu item
      "menuitemradio",
      // Radio-style menu item (selectable)
      "menuitemcheckbox",
      // Checkbox-style menu item (toggleable)
      "radio",
      // Radio button (selectable)
      "checkbox",
      // Checkbox (toggleable)
      "tab",
      // Tab (clickable to switch content)
      "switch",
      // Toggle switch (clickable to change state)
      "slider",
      // Slider control (draggable)
      "spinbutton",
      // Number input with up/down controls
      "combobox",
      // Dropdown with text input
      "searchbox",
      // Search input field
      "textbox",
      // Text input field
      "listbox",
      // Selectable list
      "option",
      // Selectable option in a list
      "scrollbar"
      // Scrollable control
    ]);
    const hasInteractiveRole = interactiveElements.has(tagName) || role && interactiveRoles.has(role) || ariaRole && interactiveRoles.has(ariaRole);
    if (hasInteractiveRole) return true;
    try {
      if (typeof getEventListeners === "function") {
        const listeners = getEventListeners(element);
        const mouseEvents = ["click", "mousedown", "mouseup", "dblclick"];
        for (const eventType of mouseEvents) {
          if (listeners[eventType] && listeners[eventType].length > 0) {
            return true;
          }
        }
      }
      const getEventListenersForNode = element?.ownerDocument?.defaultView?.getEventListenersForNode || window.getEventListenersForNode;
      if (typeof getEventListenersForNode === "function") {
        const listeners = getEventListenersForNode(element);
        const interactionEvents = [
          "click",
          "mousedown",
          "mouseup",
          "keydown",
          "keyup",
          "submit",
          "change",
          "input",
          "focus",
          "blur"
        ];
        for (const eventType of interactionEvents) {
          for (const listener of listeners) {
            if (listener.type === eventType) {
              return true;
            }
          }
        }
      }
      const commonMouseAttrs = ["onclick", "onmousedown", "onmouseup", "ondblclick"];
      for (const attr of commonMouseAttrs) {
        if (element.hasAttribute(attr) || typeof element[attr] === "function") {
          return true;
        }
      }
    } catch (e) {
    }
    if (isScrollableElement(element)) {
      return true;
    }
    return false;
  }
  __name(isInteractiveElement, "isInteractiveElement");
  function isTopElement(element) {
    if (viewportExpansion === -1) {
      return true;
    }
    const rects = getCachedClientRects(element);
    if (!rects || rects.length === 0) {
      return false;
    }
    let isAnyRectInViewport = false;
    for (const rect2 of rects) {
      if (rect2.width > 0 && rect2.height > 0 && !// Only check non-empty rects
      (rect2.bottom < -viewportExpansion || rect2.top > window.innerHeight + viewportExpansion || rect2.right < -viewportExpansion || rect2.left > window.innerWidth + viewportExpansion)) {
        isAnyRectInViewport = true;
        break;
      }
    }
    if (!isAnyRectInViewport) {
      return false;
    }
    let doc = element.ownerDocument;
    if (doc !== window.document) {
      return true;
    }
    let rect = Array.from(rects).find((r) => r.width > 0 && r.height > 0);
    if (!rect) {
      return false;
    }
    const shadowRoot = element.getRootNode();
    if (shadowRoot instanceof ShadowRoot) {
      const centerX = rect.left + rect.width / 2;
      const centerY = rect.top + rect.height / 2;
      try {
        const topEl = shadowRoot.elementFromPoint(centerX, centerY);
        if (!topEl) return false;
        let current = topEl;
        while (current && current !== shadowRoot) {
          if (current === element) return true;
          current = current.parentElement;
        }
        return false;
      } catch (e) {
        return true;
      }
    }
    const margin = 5;
    const checkPoints = [
      // Initially only this was used, but it was not enough
      { x: rect.left + rect.width / 2, y: rect.top + rect.height / 2 },
      { x: rect.left + margin, y: rect.top + margin },
      // top left
      // { x: rect.right - margin, y: rect.top + margin },    // top right
      // { x: rect.left + margin, y: rect.bottom - margin },  // bottom left
      { x: rect.right - margin, y: rect.bottom - margin }
      // bottom right
    ];
    return checkPoints.some(({ x, y }) => {
      try {
        const topEl = document.elementFromPoint(x, y);
        if (!topEl) return false;
        let current = topEl;
        while (current && current !== document.documentElement) {
          if (current === element) return true;
          current = current.parentElement;
        }
        return false;
      } catch (e) {
        return true;
      }
    });
  }
  __name(isTopElement, "isTopElement");
  function isInExpandedViewport(element, viewportExpansion2) {
    if (viewportExpansion2 === -1) {
      return true;
    }
    const rects = element.getClientRects();
    if (!rects || rects.length === 0) {
      const boundingRect = getCachedBoundingRect(element);
      if (!boundingRect || boundingRect.width === 0 || boundingRect.height === 0) {
        return false;
      }
      return !(boundingRect.bottom < -viewportExpansion2 || boundingRect.top > window.innerHeight + viewportExpansion2 || boundingRect.right < -viewportExpansion2 || boundingRect.left > window.innerWidth + viewportExpansion2);
    }
    for (const rect of rects) {
      if (rect.width === 0 || rect.height === 0) continue;
      if (!(rect.bottom < -viewportExpansion2 || rect.top > window.innerHeight + viewportExpansion2 || rect.right < -viewportExpansion2 || rect.left > window.innerWidth + viewportExpansion2)) {
        return true;
      }
    }
    return false;
  }
  __name(isInExpandedViewport, "isInExpandedViewport");
  function isInteractiveCandidate(element) {
    if (!element || element.nodeType !== Node.ELEMENT_NODE) return false;
    const tagName = element.tagName.toLowerCase();
    const interactiveElements = /* @__PURE__ */ new Set([
      "a",
      "button",
      "input",
      "select",
      "textarea",
      "details",
      "summary",
      "label"
    ]);
    if (interactiveElements.has(tagName)) return true;
    const hasQuickInteractiveAttr = element.hasAttribute("onclick") || element.hasAttribute("role") || element.hasAttribute("tabindex") || element.hasAttribute("aria-") || element.hasAttribute("data-action") || element.getAttribute("contenteditable") === "true";
    return hasQuickInteractiveAttr;
  }
  __name(isInteractiveCandidate, "isInteractiveCandidate");
  const DISTINCT_INTERACTIVE_TAGS = /* @__PURE__ */ new Set([
    "a",
    "button",
    "input",
    "select",
    "textarea",
    "summary",
    "details",
    "label",
    "option"
  ]);
  const INTERACTIVE_ROLES = /* @__PURE__ */ new Set([
    "button",
    "link",
    "menuitem",
    "menuitemradio",
    "menuitemcheckbox",
    "radio",
    "checkbox",
    "tab",
    "switch",
    "slider",
    "spinbutton",
    "combobox",
    "searchbox",
    "textbox",
    "listbox",
    "option",
    "scrollbar"
  ]);
  function isHeuristicallyInteractive(element) {
    if (!element || element.nodeType !== Node.ELEMENT_NODE) return false;
    if (!isElementVisible(element)) return false;
    const hasInteractiveAttributes = element.hasAttribute("role") || element.hasAttribute("tabindex") || element.hasAttribute("onclick") || typeof element.onclick === "function";
    const hasInteractiveClass = /\b(btn|clickable|menu|item|entry|link)\b/i.test(
      element.className || ""
    );
    const isInKnownContainer = Boolean(
      element.closest('button,a,[role="button"],.menu,.dropdown,.list,.toolbar')
    );
    const hasVisibleChildren = [...element.children].some(isElementVisible);
    const isParentBody = element.parentElement && element.parentElement.isSameNode(document.body);
    return (isInteractiveElement(element) || hasInteractiveAttributes || hasInteractiveClass) && hasVisibleChildren && isInKnownContainer && !isParentBody;
  }
  __name(isHeuristicallyInteractive, "isHeuristicallyInteractive");
  function isElementDistinctInteraction(element) {
    if (!element || element.nodeType !== Node.ELEMENT_NODE) {
      return false;
    }
    const tagName = element.tagName.toLowerCase();
    const role = element.getAttribute("role");
    if (tagName === "iframe") {
      return true;
    }
    if (DISTINCT_INTERACTIVE_TAGS.has(tagName)) {
      return true;
    }
    if (role && INTERACTIVE_ROLES.has(role)) {
      return true;
    }
    if (element.isContentEditable || element.getAttribute("contenteditable") === "true") {
      return true;
    }
    if (element.hasAttribute("data-testid") || element.hasAttribute("data-cy") || element.hasAttribute("data-test")) {
      return true;
    }
    if (element.hasAttribute("onclick") || typeof element.onclick === "function") {
      return true;
    }
    try {
      const getEventListenersForNode = element?.ownerDocument?.defaultView?.getEventListenersForNode || window.getEventListenersForNode;
      if (typeof getEventListenersForNode === "function") {
        const listeners = getEventListenersForNode(element);
        const interactionEvents = [
          "click",
          "mousedown",
          "mouseup",
          "keydown",
          "keyup",
          "submit",
          "change",
          "input",
          "focus",
          "blur"
        ];
        for (const eventType of interactionEvents) {
          for (const listener of listeners) {
            if (listener.type === eventType) {
              return true;
            }
          }
        }
      }
      const commonEventAttrs = [
        "onmousedown",
        "onmouseup",
        "onkeydown",
        "onkeyup",
        "onsubmit",
        "onchange",
        "oninput",
        "onfocus",
        "onblur"
      ];
      if (commonEventAttrs.some((attr) => element.hasAttribute(attr))) {
        return true;
      }
    } catch (e) {
    }
    if (isHeuristicallyInteractive(element)) {
      return true;
    }
    return false;
  }
  __name(isElementDistinctInteraction, "isElementDistinctInteraction");
  function handleHighlighting(nodeData, node, parentIframe, isParentHighlighted) {
    if (!nodeData.isInteractive) return false;
    let shouldHighlight = false;
    if (!isParentHighlighted) {
      shouldHighlight = true;
    } else {
      if (isElementDistinctInteraction(node)) {
        shouldHighlight = true;
      } else {
        shouldHighlight = false;
      }
    }
    if (shouldHighlight) {
      nodeData.isInViewport = isInExpandedViewport(node, viewportExpansion);
      if (nodeData.isInViewport || viewportExpansion === -1) {
        nodeData.highlightIndex = highlightIndex++;
        if (doHighlightElements) {
          if (focusHighlightIndex >= 0) {
            if (focusHighlightIndex === nodeData.highlightIndex) {
              highlightElement(node, nodeData.highlightIndex, parentIframe);
            }
          } else {
            highlightElement(node, nodeData.highlightIndex, parentIframe);
          }
          return true;
        }
      }
    }
    return false;
  }
  __name(handleHighlighting, "handleHighlighting");
  function buildDomTree(node, parentIframe = null, isParentHighlighted = false) {
    if (!node || node.id === HIGHLIGHT_CONTAINER_ID || node.nodeType !== Node.ELEMENT_NODE && node.nodeType !== Node.TEXT_NODE) {
      return null;
    }
    if (!node || node.id === HIGHLIGHT_CONTAINER_ID) {
      return null;
    }
    if (node.dataset?.browserUseIgnore === "true" || node.dataset?.pageAgentIgnore === "true") {
      return null;
    }
    if (node.getAttribute && node.getAttribute("aria-hidden") === "true") {
      return null;
    }
    if (node === document.body) {
      const nodeData2 = {
        tagName: "body",
        attributes: {},
        xpath: "/body",
        children: []
      };
      for (const child of node.childNodes) {
        const domElement = buildDomTree(child, parentIframe, false);
        if (domElement) nodeData2.children.push(domElement);
      }
      const id2 = `${ID.current++}`;
      DOM_HASH_MAP[id2] = nodeData2;
      return id2;
    }
    if (node.nodeType !== Node.ELEMENT_NODE && node.nodeType !== Node.TEXT_NODE) {
      return null;
    }
    if (node.nodeType === Node.TEXT_NODE) {
      const textContent = node.textContent?.trim();
      if (!textContent) {
        return null;
      }
      const parentElement = node.parentElement;
      if (!parentElement || parentElement.tagName.toLowerCase() === "script") {
        return null;
      }
      const id2 = `${ID.current++}`;
      DOM_HASH_MAP[id2] = {
        type: "TEXT_NODE",
        text: textContent,
        isVisible: isTextNodeVisible(node)
      };
      return id2;
    }
    if (node.nodeType === Node.ELEMENT_NODE && !isElementAccepted(node)) {
      return null;
    }
    if (viewportExpansion !== -1 && !node.shadowRoot) {
      const rect = getCachedBoundingRect(node);
      const style = getCachedComputedStyle(node);
      const isFixedOrSticky = style && (style.position === "fixed" || style.position === "sticky");
      const hasSize = node.offsetWidth > 0 || node.offsetHeight > 0;
      if (!rect || !isFixedOrSticky && !hasSize && (rect.bottom < -viewportExpansion || rect.top > window.innerHeight + viewportExpansion || rect.right < -viewportExpansion || rect.left > window.innerWidth + viewportExpansion)) {
        return null;
      }
    }
    const nodeData = {
      tagName: node.tagName.toLowerCase(),
      attributes: {},
      /**
       * @edit no need for xpath
       */
      // xpath: getXPathTree(node, true),
      children: []
    };
    if (isInteractiveCandidate(node) || node.tagName.toLowerCase() === "iframe" || node.tagName.toLowerCase() === "body") {
      const attributeNames = node.getAttributeNames?.() || [];
      for (const name of attributeNames) {
        const value = node.getAttribute(name);
        nodeData.attributes[name] = value;
      }
      if (node.tagName.toLowerCase() === "input" && (node.type === "checkbox" || node.type === "radio")) {
        nodeData.attributes.checked = node.checked ? "true" : "false";
      }
    }
    let nodeWasHighlighted = false;
    if (node.nodeType === Node.ELEMENT_NODE) {
      nodeData.isVisible = isElementVisible(node);
      if (nodeData.isVisible) {
        nodeData.isTopElement = isTopElement(node);
        const role = node.getAttribute("role");
        const isMenuContainer = role === "menu" || role === "menubar" || role === "listbox";
        if (nodeData.isTopElement || isMenuContainer) {
          nodeData.isInteractive = isInteractiveElement(node);
          nodeWasHighlighted = handleHighlighting(nodeData, node, parentIframe, isParentHighlighted);
          nodeData.ref = node;
        }
      }
    }
    if (node.tagName) {
      const tagName = node.tagName.toLowerCase();
      if (tagName === "iframe") {
        try {
          const iframeDoc = node.contentDocument || node.contentWindow?.document;
          if (iframeDoc) {
            for (const child of iframeDoc.childNodes) {
              const domElement = buildDomTree(child, node, false);
              if (domElement) nodeData.children.push(domElement);
            }
          }
        } catch (e) {
          console.warn("Unable to access iframe:", e);
        }
      } else if (node.isContentEditable || node.getAttribute("contenteditable") === "true" || node.id === "tinymce" || node.classList.contains("mce-content-body") || tagName === "body" && node.getAttribute("data-id")?.startsWith("mce_")) {
        for (const child of node.childNodes) {
          const domElement = buildDomTree(child, parentIframe, nodeWasHighlighted);
          if (domElement) nodeData.children.push(domElement);
        }
      } else {
        if (node.shadowRoot) {
          nodeData.shadowRoot = true;
          for (const child of node.shadowRoot.childNodes) {
            const domElement = buildDomTree(child, parentIframe, nodeWasHighlighted);
            if (domElement) nodeData.children.push(domElement);
          }
        }
        for (const child of node.childNodes) {
          const passHighlightStatusToChild = nodeWasHighlighted || isParentHighlighted;
          const domElement = buildDomTree(child, parentIframe, passHighlightStatusToChild);
          if (domElement) nodeData.children.push(domElement);
        }
      }
    }
    if (nodeData.tagName === "a" && nodeData.children.length === 0 && !nodeData.attributes.href) {
      const rect = getCachedBoundingRect(node);
      const hasSize = rect && rect.width > 0 && rect.height > 0 || node.offsetWidth > 0 || node.offsetHeight > 0;
      if (!hasSize) {
        return null;
      }
    }
    nodeData.extra = extraData.get(node) || null;
    const id = `${ID.current++}`;
    DOM_HASH_MAP[id] = nodeData;
    return id;
  }
  __name(buildDomTree, "buildDomTree");
  const rootId = buildDomTree(document.body);
  DOM_CACHE.clearCache();
  return { rootId, map: DOM_HASH_MAP };
}, "domTree");
const DEFAULT_VIEWPORT_EXPANSION = -1;
function resolveViewportExpansion(viewportExpansion) {
  return viewportExpansion ?? DEFAULT_VIEWPORT_EXPANSION;
}
__name(resolveViewportExpansion, "resolveViewportExpansion");
const newElementsCache = /* @__PURE__ */ new WeakMap();
function getFlatTree(config) {
  const viewportExpansion = resolveViewportExpansion(config.viewportExpansion);
  const interactiveBlacklist = [];
  for (const item of config.interactiveBlacklist || []) {
    if (typeof item === "function") {
      interactiveBlacklist.push(item());
    } else {
      interactiveBlacklist.push(item);
    }
  }
  const interactiveWhitelist = [];
  for (const item of config.interactiveWhitelist || []) {
    if (typeof item === "function") {
      interactiveWhitelist.push(item());
    } else {
      interactiveWhitelist.push(item);
    }
  }
  const elements = domTree({
    doHighlightElements: true,
    debugMode: true,
    focusHighlightIndex: -1,
    viewportExpansion,
    interactiveBlacklist,
    interactiveWhitelist,
    highlightOpacity: config.highlightOpacity ?? 0,
    highlightLabelOpacity: config.highlightLabelOpacity ?? 0.1
  });
  const currentUrl = window.location.href;
  for (const nodeId in elements.map) {
    const node = elements.map[nodeId];
    if (node.isInteractive && node.ref) {
      const ref = node.ref;
      if (!newElementsCache.has(ref)) {
        newElementsCache.set(ref, currentUrl);
        node.isNew = true;
      }
    }
  }
  return elements;
}
__name(getFlatTree, "getFlatTree");
const globRegexCache = /* @__PURE__ */ new Map();
function globToRegex(pattern) {
  let regex = globRegexCache.get(pattern);
  if (!regex) {
    const escaped = pattern.replace(/[.+^${}()|[\]\\]/g, "\\$&");
    regex = new RegExp(`^${escaped.replace(/\*/g, ".*")}$`);
    globRegexCache.set(pattern, regex);
  }
  return regex;
}
__name(globToRegex, "globToRegex");
function matchAttributes(attrs, patterns) {
  const result2 = {};
  for (const pattern of patterns) {
    if (pattern.includes("*")) {
      const regex = globToRegex(pattern);
      for (const key of Object.keys(attrs)) {
        if (regex.test(key) && attrs[key].trim()) {
          result2[key] = attrs[key].trim();
        }
      }
    } else {
      const value = attrs[pattern];
      if (value && value.trim()) {
        result2[pattern] = value.trim();
      }
    }
  }
  return result2;
}
__name(matchAttributes, "matchAttributes");
function flatTreeToString(flatTree, includeAttributes) {
  const DEFAULT_INCLUDE_ATTRIBUTES = [
    "title",
    "type",
    "checked",
    "name",
    "role",
    "value",
    "placeholder",
    "data-date-format",
    "alt",
    "aria-label",
    "aria-expanded",
    "data-state",
    "aria-checked",
    // @edit added for better form handling
    "id",
    "for",
    // for jump check
    "target",
    // absolute position dropdown menu
    "aria-haspopup",
    "aria-controls",
    "aria-owns",
    // content editable
    "contenteditable"
  ];
  const includeAttrs = [...includeAttributes || [], ...DEFAULT_INCLUDE_ATTRIBUTES];
  const capTextLength = /* @__PURE__ */ __name((text, maxLength) => {
    if (text.length > maxLength) {
      return text.substring(0, maxLength) + "...";
    }
    return text;
  }, "capTextLength");
  const buildTreeNode = /* @__PURE__ */ __name((nodeId) => {
    const node = flatTree.map[nodeId];
    if (!node) return null;
    if (node.type === "TEXT_NODE") {
      const textNode = node;
      return {
        type: "text",
        text: textNode.text,
        isVisible: textNode.isVisible,
        parent: null,
        children: []
      };
    } else {
      const elementNode = node;
      const children = [];
      if (elementNode.children) {
        for (const childId of elementNode.children) {
          const child = buildTreeNode(childId);
          if (child) {
            child.parent = null;
            children.push(child);
          }
        }
      }
      return {
        type: "element",
        tagName: elementNode.tagName,
        attributes: elementNode.attributes ?? {},
        isVisible: elementNode.isVisible ?? false,
        isInteractive: elementNode.isInteractive ?? false,
        isTopElement: elementNode.isTopElement ?? false,
        isNew: elementNode.isNew ?? false,
        highlightIndex: elementNode.highlightIndex,
        parent: null,
        children,
        extra: elementNode.extra ?? {}
      };
    }
  }, "buildTreeNode");
  const setParentReferences = /* @__PURE__ */ __name((node, parent = null) => {
    node.parent = parent;
    for (const child of node.children) {
      setParentReferences(child, node);
    }
  }, "setParentReferences");
  const rootNode = buildTreeNode(flatTree.rootId);
  if (!rootNode) return "";
  setParentReferences(rootNode);
  const hasParentWithHighlightIndex = /* @__PURE__ */ __name((node) => {
    let current = node.parent;
    while (current) {
      if (current.type === "element" && current.highlightIndex !== void 0) {
        return true;
      }
      current = current.parent;
    }
    return false;
  }, "hasParentWithHighlightIndex");
  const processNode = /* @__PURE__ */ __name((node, depth, result22) => {
    let nextDepth = depth;
    const depthStr = "	".repeat(depth);
    if (node.type === "element") {
      if (node.highlightIndex !== void 0) {
        nextDepth += 1;
        const text = getAllTextTillNextClickableElement(node);
        let attributesHtmlStr = "";
        if (includeAttrs.length > 0 && node.attributes) {
          const attributesToInclude = matchAttributes(node.attributes, includeAttrs);
          const keys = Object.keys(attributesToInclude);
          if (keys.length > 1) {
            const keysToRemove = /* @__PURE__ */ new Set();
            const seenValues = {};
            for (const key of keys) {
              const value = attributesToInclude[key];
              if (value.length > 5) {
                if (value in seenValues) {
                  keysToRemove.add(key);
                } else {
                  seenValues[value] = key;
                }
              }
            }
            for (const key of keysToRemove) {
              delete attributesToInclude[key];
            }
          }
          if (attributesToInclude.role === node.tagName) {
            delete attributesToInclude.role;
          }
          const attrsToRemoveIfTextMatches = ["aria-label", "placeholder", "title"];
          for (const attr of attrsToRemoveIfTextMatches) {
            if (attributesToInclude[attr] && attributesToInclude[attr].toLowerCase().trim() === text.toLowerCase().trim()) {
              delete attributesToInclude[attr];
            }
          }
          if (Object.keys(attributesToInclude).length > 0) {
            attributesHtmlStr = Object.entries(attributesToInclude).map(([key, value]) => `${key}=${capTextLength(value, 20)}`).join(" ");
          }
        }
        const highlightIndicator = node.isNew ? `*[${node.highlightIndex}]` : `[${node.highlightIndex}]`;
        let line = `${depthStr}${highlightIndicator}<${node.tagName ?? ""}`;
        if (attributesHtmlStr) {
          line += ` ${attributesHtmlStr}`;
        }
        if (node.extra) {
          if (node.extra.scrollable) {
            let scrollDataText = "";
            if (node.extra.scrollData?.left)
              scrollDataText += `left=${node.extra.scrollData.left}, `;
            if (node.extra.scrollData?.top) scrollDataText += `top=${node.extra.scrollData.top}, `;
            if (node.extra.scrollData?.right)
              scrollDataText += `right=${node.extra.scrollData.right}, `;
            if (node.extra.scrollData?.bottom)
              scrollDataText += `bottom=${node.extra.scrollData.bottom}`;
            line += ` data-scrollable="${scrollDataText}"`;
          }
        }
        if (text) {
          const trimmedText = text.trim();
          if (!attributesHtmlStr) {
            line += " ";
          }
          line += `>${trimmedText}`;
        } else if (!attributesHtmlStr) {
          line += " ";
        }
        line += " />";
        result22.push(line);
      }
      for (const child of node.children) {
        processNode(child, nextDepth, result22);
      }
    } else if (node.type === "text") {
      if (hasParentWithHighlightIndex(node)) {
        return;
      }
      if (node.parent && node.parent.type === "element" && node.parent.isVisible && node.parent.isTopElement) {
        result22.push(`${depthStr}${node.text ?? ""}`);
      }
    }
  }, "processNode");
  const result2 = [];
  processNode(rootNode, 0, result2);
  return result2.join("\n");
}
__name(flatTreeToString, "flatTreeToString");
const getAllTextTillNextClickableElement = /* @__PURE__ */ __name((node, maxDepth = -1) => {
  const textParts = [];
  const collectText = /* @__PURE__ */ __name((currentNode, currentDepth) => {
    if (maxDepth !== -1 && currentDepth > maxDepth) {
      return;
    }
    if (currentNode.type === "element" && currentNode !== node && currentNode.highlightIndex !== void 0) {
      return;
    }
    if (currentNode.type === "text" && currentNode.text) {
      textParts.push(currentNode.text);
    } else if (currentNode.type === "element") {
      for (const child of currentNode.children) {
        collectText(child, currentDepth + 1);
      }
    }
  }, "collectText");
  collectText(node, 0);
  return textParts.join("\n").trim();
}, "getAllTextTillNextClickableElement");
function getSelectorMap(flatTree) {
  const selectorMap = /* @__PURE__ */ new Map();
  const keys = Object.keys(flatTree.map);
  for (const key of keys) {
    const node = flatTree.map[key];
    if (node.isInteractive && typeof node.highlightIndex === "number") {
      selectorMap.set(node.highlightIndex, node);
    }
  }
  return selectorMap;
}
__name(getSelectorMap, "getSelectorMap");
function getElementTextMap(simplifiedHTML) {
  const lines = simplifiedHTML.split("\n").map((line) => line.trim()).filter((line) => line.length > 0);
  const elementTextMap = /* @__PURE__ */ new Map();
  for (const line of lines) {
    const regex = /^\[(\d+)\]<[^>]+>([^<]*)/;
    const match = regex.exec(line);
    if (match) {
      const index = parseInt(match[1], 10);
      elementTextMap.set(index, line);
    }
  }
  return elementTextMap;
}
__name(getElementTextMap, "getElementTextMap");
function cleanUpHighlights() {
  const cleanupFunctions = window._highlightCleanupFunctions || [];
  for (const cleanup of cleanupFunctions) {
    if (typeof cleanup === "function") {
      cleanup();
    }
  }
  window._highlightCleanupFunctions = [];
}
__name(cleanUpHighlights, "cleanUpHighlights");
window.addEventListener("popstate", () => {
  cleanUpHighlights();
});
window.addEventListener("hashchange", () => {
  cleanUpHighlights();
});
window.addEventListener("beforeunload", () => {
  cleanUpHighlights();
});
const navigation = window.navigation;
if (navigation && typeof navigation.addEventListener === "function") {
  navigation.addEventListener("navigate", () => {
    cleanUpHighlights();
  });
} else {
  let currentUrl = window.location.href;
  setInterval(() => {
    if (window.location.href !== currentUrl) {
      currentUrl = window.location.href;
      cleanUpHighlights();
    }
  }, 500);
}
function getPageInfo() {
  const viewport_width = window.innerWidth;
  const viewport_height = window.innerHeight;
  const page_width = Math.max(document.documentElement.scrollWidth, document.body.scrollWidth || 0);
  const page_height = Math.max(
    document.documentElement.scrollHeight,
    document.body.scrollHeight || 0
  );
  const scroll_x = window.scrollX || window.pageXOffset || document.documentElement.scrollLeft || 0;
  const scroll_y = window.scrollY || window.pageYOffset || document.documentElement.scrollTop || 0;
  const pixels_below = Math.max(0, page_height - (window.innerHeight + scroll_y));
  const pixels_right = Math.max(0, page_width - (window.innerWidth + scroll_x));
  return {
    // Current viewport dimensions
    viewport_width,
    viewport_height,
    // Total page dimensions
    page_width,
    page_height,
    // Current scroll position
    scroll_x,
    scroll_y,
    pixels_above: scroll_y,
    pixels_below,
    pages_above: viewport_height > 0 ? scroll_y / viewport_height : 0,
    pages_below: viewport_height > 0 ? pixels_below / viewport_height : 0,
    total_pages: viewport_height > 0 ? page_height / viewport_height : 0,
    current_page_position: scroll_y / Math.max(1, page_height - viewport_height),
    pixels_left: scroll_x,
    pixels_right
  };
}
__name(getPageInfo, "getPageInfo");
function patchReact(pageController) {
  const reactRootElements = document.querySelectorAll(
    '[data-reactroot], [data-reactid], [data-react-checksum], #root, #app, [id^="root-"], [id^="app-"], #adex-wrapper, #adex-root'
  );
  for (const element of reactRootElements) {
    element.setAttribute("data-page-agent-not-interactive", "true");
  }
}
__name(patchReact, "patchReact");
const _PageController = class _PageController extends EventTarget {
  config;
  /** Corresponds to eval_page in browser-use */
  flatTree = null;
  /**
   * All highlighted index-mapped interactive elements
   * Corresponds to DOMState.selector_map in browser-use
   */
  selectorMap = /* @__PURE__ */ new Map();
  /** Index -> element text description mapping */
  elementTextMap = /* @__PURE__ */ new Map();
  /**
   * Simplified HTML for LLM consumption.
   * Corresponds to clickable_elements_to_string in browser-use
   */
  simplifiedHTML = "<EMPTY>";
  /** last time the tree was updated */
  lastTimeUpdate = 0;
  /** Whether the tree has been indexed at least once */
  isIndexed = false;
  /** Visual mask overlay for blocking user interaction during automation */
  mask = null;
  maskReady = null;
  constructor(config = {}) {
    super();
    this.config = config;
    patchReact();
    if (config.enableMask) this.initMask();
  }
  /**
   * Initialize mask asynchronously (dynamic import to avoid CSS loading in Node)
   */
  initMask() {
    if (this.maskReady !== null) return;
    this.maskReady = (async () => {
      const { SimulatorMask } = await import("./SimulatorMask-C7yoC9Lw.js");
      this.mask = new SimulatorMask();
    })();
  }
  // ======= State Queries =======
  /**
   * Get current page URL
   */
  async getCurrentUrl() {
    return window.location.href;
  }
  /**
   * Get last tree update timestamp
   */
  async getLastUpdateTime() {
    return this.lastTimeUpdate;
  }
  /**
   * Get structured browser state for LLM consumption.
   * Automatically calls updateTree() to refresh the DOM state.
   */
  async getBrowserState() {
    const url = window.location.href;
    const title = document.title;
    const pi = getPageInfo();
    const viewportExpansion = resolveViewportExpansion(this.config.viewportExpansion);
    await this.updateTree();
    const content = this.simplifiedHTML;
    const titleLine = `Current Page: [${title}](${url})`;
    const pageInfoLine = `Page info: ${pi.viewport_width}x${pi.viewport_height}px viewport, ${pi.page_width}x${pi.page_height}px total page size, ${pi.pages_above.toFixed(1)} pages above, ${pi.pages_below.toFixed(1)} pages below, ${pi.total_pages.toFixed(1)} total pages, at ${(pi.current_page_position * 100).toFixed(0)}% of page`;
    const elementsLabel = viewportExpansion === -1 ? "Interactive elements from top layer of the current page (full page):" : "Interactive elements from top layer of the current page inside the viewport:";
    const hasContentAbove = pi.pixels_above > 4;
    const scrollHintAbove = hasContentAbove && viewportExpansion !== -1 ? `... ${pi.pixels_above} pixels above (${pi.pages_above.toFixed(1)} pages) - scroll to see more ...` : "[Start of page]";
    const header = `${titleLine}
${pageInfoLine}

${elementsLabel}

${scrollHintAbove}`;
    const hasContentBelow = pi.pixels_below > 4;
    const footer = hasContentBelow && viewportExpansion !== -1 ? `... ${pi.pixels_below} pixels below (${pi.pages_below.toFixed(1)} pages) - scroll to see more ...` : "[End of page]";
    return { url, title, header, content, footer };
  }
  // ======= DOM Tree Operations =======
  /**
   * Update DOM tree, returns simplified HTML for LLM.
   * This is the main method to refresh the page state.
   * Automatically bypasses mask during DOM extraction if enabled.
   */
  async updateTree() {
    this.dispatchEvent(new Event("beforeUpdate"));
    this.lastTimeUpdate = Date.now();
    if (this.mask) {
      this.mask.wrapper.style.pointerEvents = "none";
    }
    cleanUpHighlights();
    const blacklist = [
      ...this.config.interactiveBlacklist || [],
      ...document.querySelectorAll("[data-page-agent-not-interactive]").values()
    ];
    this.flatTree = getFlatTree({
      ...this.config,
      interactiveBlacklist: blacklist
    });
    this.simplifiedHTML = flatTreeToString(this.flatTree, this.config.includeAttributes);
    this.selectorMap.clear();
    this.selectorMap = getSelectorMap(this.flatTree);
    this.elementTextMap.clear();
    this.elementTextMap = getElementTextMap(this.simplifiedHTML);
    this.isIndexed = true;
    if (this.mask) {
      this.mask.wrapper.style.pointerEvents = "auto";
    }
    this.dispatchEvent(new Event("afterUpdate"));
    return this.simplifiedHTML;
  }
  /**
   * Clean up all element highlights
   */
  async cleanUpHighlights() {
    cleanUpHighlights();
  }
  // ======= Element Actions =======
  /**
   * Ensure the tree has been indexed before any index-based operation.
   * Throws if updateTree() hasn't been called yet.
   */
  assertIndexed() {
    if (!this.isIndexed) {
      throw new Error("DOM tree not indexed yet. Can not perform actions on elements.");
    }
  }
  /**
   * Click element by index
   */
  async clickElement(index) {
    try {
      this.assertIndexed();
      const element = getElementByIndex(this.selectorMap, index);
      const elemText = this.elementTextMap.get(index);
      await clickElement(element);
      if (element instanceof HTMLAnchorElement && element.target === "_blank") {
        return {
          success: true,
          message: `✅ Clicked element (${elemText ?? index}). ⚠️ Link opened in a new tab.`
        };
      }
      return {
        success: true,
        message: `✅ Clicked element (${elemText ?? index}).`
      };
    } catch (error) {
      return {
        success: false,
        message: `❌ Failed to click element: ${error}`
      };
    }
  }
  /**
   * Input text into element by index
   */
  async inputText(index, text) {
    try {
      this.assertIndexed();
      const element = getElementByIndex(this.selectorMap, index);
      const elemText = this.elementTextMap.get(index);
      await inputTextElement(element, text);
      return {
        success: true,
        message: `✅ Input text (${text}) into element (${elemText ?? index}).`
      };
    } catch (error) {
      return {
        success: false,
        message: `❌ Failed to input text: ${error}`
      };
    }
  }
  /**
   * Select dropdown option by index and option text
   */
  async selectOption(index, optionText) {
    try {
      this.assertIndexed();
      const element = getElementByIndex(this.selectorMap, index);
      const elemText = this.elementTextMap.get(index);
      await selectOptionElement(element, optionText);
      return {
        success: true,
        message: `✅ Selected option (${optionText}) in element (${elemText ?? index}).`
      };
    } catch (error) {
      return {
        success: false,
        message: `❌ Failed to select option: ${error}`
      };
    }
  }
  /**
   * Scroll vertically
   */
  async scroll(options) {
    try {
      const { down, numPages, pixels, index } = options;
      this.assertIndexed();
      const scrollAmount = pixels ?? numPages * (down ? 1 : -1) * window.innerHeight;
      const element = index !== void 0 ? getElementByIndex(this.selectorMap, index) : null;
      const message = await scrollVertically(down, scrollAmount, element);
      return {
        success: true,
        message
      };
    } catch (error) {
      return {
        success: false,
        message: `❌ Failed to scroll: ${error}`
      };
    }
  }
  /**
   * Scroll horizontally
   */
  async scrollHorizontally(options) {
    try {
      const { right, pixels, index } = options;
      this.assertIndexed();
      const scrollAmount = pixels * (right ? 1 : -1);
      const element = index !== void 0 ? getElementByIndex(this.selectorMap, index) : null;
      const message = await scrollHorizontally(right, scrollAmount, element);
      return {
        success: true,
        message
      };
    } catch (error) {
      return {
        success: false,
        message: `❌ Failed to scroll horizontally: ${error}`
      };
    }
  }
  /**
   * Execute arbitrary JavaScript on the page
   */
  async executeJavascript(script) {
    try {
      const asyncFunction = eval(`(async () => { ${script} })`);
      const result = await asyncFunction();
      return {
        success: true,
        message: `✅ Executed JavaScript. Result: ${result}`
      };
    } catch (error) {
      return {
        success: false,
        message: `❌ Error executing JavaScript: ${error}`
      };
    }
  }
  // ======= Mask Operations =======
  /**
   * Show the visual mask overlay.
   * Only works after mask is setup.
   */
  async showMask() {
    await this.maskReady;
    this.mask?.show();
  }
  /**
   * Hide the visual mask overlay.
   * Only works after mask is setup.
   */
  async hideMask() {
    await this.maskReady;
    this.mask?.hide();
  }
  /**
   * Dispose and clean up resources
   */
  dispose() {
    cleanUpHighlights();
    this.flatTree = null;
    this.selectorMap.clear();
    this.elementTextMap.clear();
    this.simplifiedHTML = "<EMPTY>";
    this.isIndexed = false;
    this.mask?.dispose();
    this.mask = null;
  }
};
__name(_PageController, "PageController");
let PageController = _PageController;
export {
  PageController
};
//# sourceMappingURL=page-controller.js.map
