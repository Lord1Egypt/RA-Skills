from __future__ import annotations

import json
import time
from typing import Any

from .bridge import BridgePage
from .browser_urls import build_category_suggest_url, build_post_ad_create_url
from .errors import BrowserAutomationError

_FETCH_CATEGORY_SUGGEST_JS = """
((apiUrl) => {
  return fetch(apiUrl, {
    method: "GET",
    credentials: "include",
    headers: { "Accept": "application/json" },
  })
    .then((res) => {
      if (!res.ok) {
        throw new Error("类目建议 API 返回 " + res.status);
      }
      return res.json();
    })
    .then((data) => JSON.stringify(data));
})
"""

_EXTRACT_POST_AD_FIELDS_JS = """
(async () => {
  const form = document.querySelector("#syi-form") || document.querySelector("form");
  if (!form) {
    throw new Error("未找到发布表单");
  }

  const clean = (value) => (value || "").replace(/\\s+/g, " ").trim();
  const sleep = (ms) => new Promise((resolve) => setTimeout(resolve, ms));

  const isVisible = (el) => {
    if (!(el instanceof HTMLElement)) return false;
    if (el.hidden) return false;
    const style = window.getComputedStyle(el);
    if (style.display === "none" || style.visibility === "hidden") return false;
    return !!(el.offsetWidth || el.offsetHeight || el.getClientRects().length);
  };

  const getPanel = (el) => {
    const panel =
      el.closest("[data-validation-group]") ||
      el.closest(".panel") ||
      el.closest("fieldset");
    if (!panel) return "";
    const heading = panel.querySelector("h1, h2, h3, h4, legend");
    const panelName =
      panel.getAttribute("data-validation-group") ||
      panel.getAttribute("data-panel-name") ||
      "";
    return clean(heading?.textContent || panelName);
  };

  const getLabel = (el) => {
    const id = el.getAttribute("id");
    const directLabel = id
      ? document.querySelector(`label[for="${CSS.escape(id)}"]`)
      : null;
    if (directLabel) return clean(directLabel.textContent);

    const wrappingLabel = el.closest("label");
    if (wrappingLabel) return clean(wrappingLabel.textContent);

    const formElement =
      el.closest(".form-element") ||
      el.closest(".field") ||
      el.closest("fieldset") ||
      el.parentElement;
    if (!formElement) return clean(el.getAttribute("aria-label") || el.getAttribute("placeholder") || el.name);

    const candidate = formElement.querySelector(
      "label, legend, [data-testid*='label'], [class*='label'], [class*='title']"
    );
    return clean(
      candidate?.textContent ||
        el.getAttribute("aria-label") ||
        el.getAttribute("placeholder") ||
        el.name
    );
  };

  const getGroupLabel = (el) => {
    const container =
      el.closest("fieldset") ||
      el.closest("[role='radiogroup']") ||
      el.closest(".form-element") ||
      el.closest(".panel");
    if (!container) return getLabel(el);
    const candidate = container.querySelector(
      "legend, h1, h2, h3, h4, [data-testid*='label'], [class*='label'], [class*='title']"
    );
    return clean(candidate?.textContent || getPanel(el) || getLabel(el));
  };

  const hasRequiredMarker = (text) => /\\*/.test(text || "");

  const isRequiredField = (el, labelText = "") =>
    !!(
      el.required ||
      el.getAttribute("aria-required") === "true" ||
      el.closest("[data-required='true']") ||
      hasRequiredMarker(labelText)
    );

  const buildOption = (input) => ({
    value: input.value,
    label: getLabel(input) || clean(input.value),
    checked: !!input.checked,
  });

  const seen = new Set();
  const fields = [];
  const dialogOptionMap = {};
  const diagnostics = {
    modal_triggers: [],
    modal_option_counts: {},
  };

  const pushField = (field) => {
    fields.push({
      ...field,
      label: clean(field.label),
      panel: clean(field.panel),
    });
    seen.add(field.name);
  };

  const findFieldContainer = (el) =>
    el.closest(".form-element") || el.closest(".panel") || el.parentElement;

  const resolveTriggerFieldName = (trigger) => {
    const container = findFieldContainer(trigger);
    if (!container) return "";

    const nearbyNamedField = container.querySelector("input[name], select[name], textarea[name]");
    if (nearbyNamedField instanceof HTMLElement) {
      return nearbyNamedField.getAttribute("name") || "";
    }

    const key = (trigger.getAttribute("data-q") || "").replace(/-modal-trigger$/, "");
    if (!key) return "";

    const exact = form.querySelector(`[name="attributes[${CSS.escape(key)}]"]`);
    if (exact instanceof HTMLElement) {
      return exact.getAttribute("name") || "";
    }

    return `attributes[${key}]`;
  };

  const clickRegularMode = async () => {
    const regular = document.querySelector('input#regular[name="attributes[mazuma_listing_options]"]');
    if (!(regular instanceof HTMLInputElement)) {
      return false;
    }
    regular.click();
    regular.checked = true;
    regular.dispatchEvent(new Event("input", { bubbles: true }));
    regular.dispatchEvent(new Event("change", { bubbles: true }));
    regular.dispatchEvent(new Event("blur", { bubbles: true }));
    return true;
  };

  const waitForFullForm = async () => {
    const deadline = Date.now() + 10000;
    while (Date.now() < deadline) {
      const titleInput = form.querySelector('input[name="title"]');
      const descriptionInput = form.querySelector('textarea[name="description"]');
      if (titleInput && descriptionInput) {
        return true;
      }
      await sleep(200);
    }
    return false;
  };

  const captureVisibleDialogOptions = () => {
    const dialog =
      document.querySelector('[role="dialog"]') ||
      document.querySelector('[data-testid="dialog-content"]') ||
      document.querySelector('.dialog-content');
    if (!(dialog instanceof HTMLElement) || !isVisible(dialog)) {
      return;
    }

    const grouped = {};
    Array.from(dialog.querySelectorAll("input, select, textarea")).forEach((el) => {
      const name = el.getAttribute("name");
      if (!name || el.disabled) return;
      const type =
        el.tagName.toLowerCase() === "input"
          ? (el.getAttribute("type") || "text").toLowerCase()
          : el.tagName.toLowerCase();
      if (type === "hidden") return;
      if (!grouped[name]) grouped[name] = [];
      grouped[name].push(el);
    });

    Object.entries(grouped).forEach(([name, nodes]) => {
      const first = nodes[0];
      const type =
        first.tagName.toLowerCase() === "input"
          ? (first.getAttribute("type") || "text").toLowerCase()
          : first.tagName.toLowerCase();

      if (type === "radio") {
        dialogOptionMap[name] = {
          type: "radio",
          options: nodes.map((node) => buildOption(node)),
        };
        return;
      }

      if (type === "select") {
        dialogOptionMap[name] = {
          type: "select",
          options: Array.from(first.querySelectorAll("option")).map((option) => ({
            value: option.value,
            label: clean(option.textContent),
            selected: option.selected,
            disabled: option.disabled,
          })),
        };
      }
    });
  };

  const closeDialog = async () => {
    const overlay = document.querySelector('[data-testid="overlay"]');
    if (overlay instanceof HTMLElement) {
      overlay.click();
      await sleep(150);
      return;
    }

    document.dispatchEvent(new KeyboardEvent("keydown", { key: "Escape", bubbles: true }));
    await sleep(150);
  };

  const expandFieldTriggers = async () => {
    const triggers = Array.from(form.querySelectorAll('button[data-q$="-modal-trigger"]'));
    for (const trigger of triggers) {
      if (!(trigger instanceof HTMLButtonElement) || !isVisible(trigger)) continue;
      diagnostics.modal_triggers.push({
        trigger: trigger.getAttribute("data-q") || "",
        text: clean(trigger.textContent || ""),
      });
      trigger.click();
      await sleep(250);
      captureVisibleDialogOptions();
      Object.entries(dialogOptionMap).forEach(([name, value]) => {
        diagnostics.modal_option_counts[name] = value.options?.length || 0;
      });
      await closeDialog();
    }
  };

  await clickRegularMode();
  await waitForFullForm();
  await sleep(300);
  await expandFieldTriggers();

  Array.from(form.querySelectorAll('button[data-q$="-modal-trigger"]')).forEach((trigger) => {
    if (!(trigger instanceof HTMLButtonElement) || !isVisible(trigger)) return;

    const name = resolveTriggerFieldName(trigger);
    if (!name || seen.has(name)) return;

    const container = findFieldContainer(trigger);
    const labelNode =
      container?.querySelector('label, [data-q$="-field-title"], [class*="label"], [class*="title"]') ||
      trigger;
    const label = clean(labelNode?.textContent || trigger.textContent || name);
    const backingField = container?.querySelector(`input[name="${CSS.escape(name)}"], select[name="${CSS.escape(name)}"], textarea[name="${CSS.escape(name)}"]`);
    const panel = container ? getPanel(container) : "";
    const options = dialogOptionMap[name]?.options || [];

    pushField({
      name,
      type: options.length ? dialogOptionMap[name]?.type || "modal_select" : "modal_select",
      label,
      panel,
      required: !!(backingField && isRequiredField(backingField, label)) || hasRequiredMarker(label),
      value:
        backingField instanceof HTMLInputElement ||
        backingField instanceof HTMLTextAreaElement ||
        backingField instanceof HTMLSelectElement
          ? backingField.value
          : "",
      placeholder: clean(trigger.textContent || ""),
      trigger: trigger.getAttribute("data-q") || "",
      options,
    });
  });

  Array.from(form.querySelectorAll("input, select, textarea")).forEach((el) => {
    const name = el.getAttribute("name");
    if (!name || seen.has(name) || el.disabled) return;

    const type =
      el.tagName.toLowerCase() === "input"
        ? (el.getAttribute("type") || "text").toLowerCase()
        : el.tagName.toLowerCase();

    if (type === "hidden") return;
    if (type !== "radio" && !isVisible(el)) return;

    if (type === "radio") {
      const radios = Array.from(
        form.querySelectorAll(`input[type="radio"][name="${CSS.escape(name)}"]`)
      );
      if (!radios.length) return;
      pushField({
        name,
        type: "radio",
        label: getGroupLabel(radios[0]),
        panel: getPanel(radios[0]),
        required: radios.some((item) => isRequiredField(item, getGroupLabel(item))),
        options: dialogOptionMap[name]?.options || radios.map(buildOption),
      });
      return;
    }

    if (type === "checkbox") {
      const checkboxes = Array.from(
        form.querySelectorAll(`input[type="checkbox"][name="${CSS.escape(name)}"]`)
      ).filter((item) => isVisible(item));
      if (checkboxes.length > 1) {
        pushField({
          name,
          type: "checkbox_group",
          label: getGroupLabel(checkboxes[0]),
          panel: getPanel(checkboxes[0]),
          required: checkboxes.some((item) => isRequiredField(item, getGroupLabel(item))),
          options: checkboxes.map(buildOption),
        });
        return;
      }
    }

    if (type === "select") {
      pushField({
        name,
        type: "select",
        label: getLabel(el),
        panel: getPanel(el),
        required: isRequiredField(el, getLabel(el)),
        options: (dialogOptionMap[name]?.options || Array.from(el.querySelectorAll("option"))
          .map((option) => ({
            value: option.value,
            label: clean(option.textContent),
            selected: option.selected,
            disabled: option.disabled,
          }))).filter((option) => option.value || option.label),
      });
      return;
    }

    pushField({
      name,
      type,
      label: getLabel(el),
      panel: getPanel(el),
      required: isRequiredField(el, getLabel(el)),
      value: "value" in el ? el.value : "",
      placeholder: el.getAttribute("placeholder") || "",
    });
  });

  const imagePanel = form.querySelector('[data-validation-group="images"][data-required="true"]');
  if (imagePanel) {
    fields.push({
      name: "images-file-input",
      type: "file",
      required: true,
      label: "Photos",
      panel: clean(getPanel(imagePanel)),
      note: "Add at least 1 image",
    });
  }

  const requiredFields = fields.filter((field) => field.required);

  return JSON.stringify({
    total_fields: fields.length,
    required_count: requiredFields.length,
    required_fields: requiredFields,
  //  all_fields: fields,
  //  diagnostics,
  });
})()
"""


def _evaluate_json(page: BridgePage, expression: str) -> dict[str, Any]:
    raw = page.evaluate(expression)
    if not raw:
        raise BrowserAutomationError("浏览器返回了空结果")
    payload = json.loads(raw)
    if not isinstance(payload, dict):
        raise BrowserAutomationError("浏览器结果格式异常")
    return payload


def _wait_for_expression(
    page: BridgePage,
    expression: str,
    timeout: float,
    interval: float,
    message: str,
) -> Any:
    deadline = time.time() + timeout
    while time.time() < deadline:
        result = page.evaluate(expression)
        if result:
            return result
        time.sleep(interval)
    raise BrowserAutomationError(message)


def _format_category(cat: dict[str, Any], index: int) -> dict[str, Any]:
    return {
        "index": index,
        "id": cat.get("id"),
        "displayName": cat.get("displayName"),
        "tree": cat.get("tree"),
    }


def _find_best_category(
    categories: list[dict[str, Any]],
    category_name: str,
) -> tuple[int, dict[str, Any]] | None:
    target = category_name.strip().lower()
    for i, cat in enumerate(categories):
        if cat.get("displayName", "").strip().lower() == target:
            return i, cat
    for i, cat in enumerate(categories):
        if target in cat.get("displayName", "").strip().lower():
            return i, cat
    for i, cat in enumerate(categories):
        if target in cat.get("tree", "").strip().lower():
            return i, cat
    return None


def _extract_post_ad_fields(page: BridgePage) -> dict[str, Any]:
    return _evaluate_json(page, _EXTRACT_POST_AD_FIELDS_JS)


def _prepare_post_ad_form(page: BridgePage) -> None:
    has_regular = page.evaluate(
        """
(() => {
  const regular = document.querySelector('input#regular[name="attributes[mazuma_listing_options]"]');
  if (!(regular instanceof HTMLInputElement)) {
    return false;
  }
  regular.click();
  regular.checked = true;
  regular.dispatchEvent(new Event("input", { bubbles: true }));
  regular.dispatchEvent(new Event("change", { bubbles: true }));
  regular.dispatchEvent(new Event("blur", { bubbles: true }));
  return true;
})()
"""
    )
    if has_regular:
        _wait_for_expression(
            page,
            """(() => Boolean(
              document.querySelector('#syi-form input[name="title"]') &&
              document.querySelector('#syi-form textarea[name="description"]')
            ))()""",
            timeout=10.0,
            interval=0.2,
            message="点击 Sell on Gumtree 后，完整发布表单未在预期时间内出现",
        )
    page.wait_dom_stable(timeout=10000)


def run_browser_post_ad_category(
    page: BridgePage,
    keyword: str,
    category_name: str | None = None,
    category_index: int | None = None,
) -> dict[str, Any]:
    api_url = build_category_suggest_url(keyword)
    result = _evaluate_json(
        page, f"{_FETCH_CATEGORY_SUGGEST_JS}({json.dumps(api_url)})"
    )

    categories = result.get("categories", [])
    display_categories = [
        _format_category(cat, i) for i, cat in enumerate(categories)
    ]

    if not categories:
        return {
            "ok": False,
            "mode": "browser",
            "keyword": keyword,
            "error": f"关键词 '{keyword}' 未返回任何建议类目",
            "categories": [],
        }

    if category_index is None and category_name is None:
        return {
            "ok": True,
            "mode": "browser",
            "step": "suggest",
            "keyword": keyword,
            "message": "已获取建议类目，请选择"
            "（传入 --category-name 或 --category-index）",
            "categories": display_categories,
        }

    selected_cat: dict[str, Any] | None = None
    selected_idx: int | None = None

    if category_index is not None:
        if category_index < 0 or category_index >= len(categories):
            return {
                "ok": False,
                "mode": "browser",
                "keyword": keyword,
                "error": (
                    f"类目索引 {category_index} 超出范围，"
                    f"共 {len(categories)} 个建议类目"
                ),
                "categories": display_categories,
            }
        selected_idx = category_index
        selected_cat = categories[category_index]
    elif category_name is not None:
        match = _find_best_category(categories, category_name)
        if match is None:
            return {
                "ok": False,
                "mode": "browser",
                "keyword": keyword,
                "error": f"未在建议类目中找到匹配 '{category_name}' 的项",
                "categories": display_categories,
            }
        selected_idx, selected_cat = match

    category_id = selected_cat["id"]
    create_url = build_post_ad_create_url(category_id)
    page.navigate(create_url)
    page.wait_for_load()
    page.wait_dom_stable(timeout=15000)
    _prepare_post_ad_form(page)

    final_url_raw = page.evaluate("window.location.href")
    final_url = (
        final_url_raw.strip('"') if isinstance(final_url_raw, str) else ""
    )
    post_ad_fields = _extract_post_ad_fields(page)

    return {
        "ok": True,
        "mode": "browser",
        "step": "category_selected",
        "keyword": keyword,
        "categories": display_categories,
        "selected_category": _format_category(selected_cat, selected_idx),
        "redirected_url": final_url,
        "post_ad_fields": post_ad_fields,
    }
