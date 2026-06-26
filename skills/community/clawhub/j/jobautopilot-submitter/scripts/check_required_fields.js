// check_required_fields.js — READ-ONLY DOM query for unfilled required form fields
//
// PURPOSE: Returns a list of required fields on the current page, grouped into
//          "unfilled" (needs input) and "filled" (for verification).
//
// SECURITY: This script is a pure DOM read. It does NOT:
//   - Modify any page content or form values
//   - Make any network requests (no fetch, XMLHttpRequest, sendBeacon, etc.)
//   - Access cookies, localStorage, or sessionStorage
//   - Exfiltrate any data from the page
//
// It is equivalent to running document.querySelectorAll("[required]") in DevTools.
// Full source is unminified and unobfuscated for easy audit.

() => {
 const fields = [];

 function getLabel(el) {
 const labelledBy = el.getAttribute("aria-labelledby");
 if (labelledBy) {
 const labelEl = document.getElementById(labelledBy.split(" ")[0]);
 if (labelEl) return labelEl.innerText.trim();
 }
 if (el.getAttribute("aria-label")) return el.getAttribute("aria-label");
 if (el.id) {
 const forLabel = document.querySelector("label[for=\"" + el.id + "\"]");
 if (forLabel) return forLabel.innerText.trim();
 }
 return el.name || el.id || "unknown field";
 }

 // Find the sentinel input inside the combobox container — framework-agnostic pattern
 
 // Most frameworks (React Select, Vue Select, Headless UI) use a hidden input with aria-hidden + tabindex="-1" to attach required validation
 function getSentinelValue(combobox) {
 // Walk up to the wrapping container (max 5 levels)
 let node = combobox.parentElement;
 for (let i = 0; i < 5; i++) {
 if (!node) break;
 const sentinel = node.querySelector(
 "input[aria-hidden=\"true\"][tabindex=\"-1\"]," +
 "input[type=\"hidden\"][required]," +
 "input[tabindex=\"-1\"][required]"
 );
 if (sentinel) return sentinel.value ? sentinel.value.trim() : null;
 node = node.parentElement;
 }
 return null;
 }

 // Find selected items in the listbox associated with this combobox
 function getAriaSelectedValues(combobox) {
 // Method 1: aria-controls pointing to a listbox
 const listboxId = combobox.getAttribute("aria-controls") ||
 combobox.getAttribute("aria-owns");
 if (listboxId) {
 const listbox = document.getElementById(listboxId);
 if (listbox) {
 const selected = listbox.querySelectorAll("[aria-selected=\"true\"]");
 if (selected.length > 0)
 return Array.from(selected).map(el => el.innerText.trim()).join(", ");
 }
 }

 // Method 2: find role="option"[aria-selected="true"] inside parent containers
 let node = combobox.parentElement;
 for (let i = 0; i < 5; i++) {
 if (!node) break;
 const selected = node.querySelectorAll("[role=\"option\"][aria-selected=\"true\"]");
 if (selected.length > 0)
 return Array.from(selected).map(el => el.innerText.trim()).join(", ");
 node = node.parentElement;
 }
 return null;
 }

 // Find the visible selected-value text inside the container (exclude the input itself, buttons, placeholders)
 function getDisplayedValue(combobox) {
 const placeholderIds = (combobox.getAttribute("aria-describedby") || "").split(" ");

 let node = combobox.parentElement;
 for (let i = 0; i < 5; i++) {
 if (!node) break;
 const candidates = node.querySelectorAll(
 "span:not([aria-hidden=\"true\"]), div:not([aria-hidden=\"true\"])"
 );
 for (const el of candidates) {
 // Exclude placeholder elements (id listed in aria-describedby)
 if (el.id && placeholderIds.includes(el.id)) continue;
 // Exclude ancestors of the input (avoid matching the combobox container itself)
 if (el.contains(combobox)) continue;
 // Exclude button/icon containers
 if (el.querySelector("button, svg")) continue;
 const text = el.innerText.trim();
 if (text) return text;
 }
 node = node.parentElement;
 }
 return null;
 }

 // 1. Native fields
 document.querySelectorAll("[required], [aria-required=\"true\"]").forEach(el => {
 if (el.getAttribute("aria-hidden") === "true") return;
 if (el.getAttribute("role") === "combobox" && el.getAttribute("aria-autocomplete") === "list") return;

 const tag = el.tagName;
 const type = (el.type || "").toLowerCase();
 let filled = false;
 let value = null;

 if (type === "checkbox" || type === "radio") {
 filled = el.checked;
 value = el.checked ? (el.value || "checked") : null;
 } else if (tag === "SELECT") {
 const opt = el.options[el.selectedIndex];
 value = opt ? opt.text.trim() : null;
 filled = !!value && value !== "";
 } else if (tag === "INPUT" || tag === "TEXTAREA") {
 value = el.value.trim() || null;
 filled = !!value;
 } else if (tag === "DIV" || tag === "SPAN") {
 const text = (el.innerText || el.textContent || "").trim();
 filled = text !== "" && !/attach|upload/i.test(text);
 value = filled ? text : null;
 }

 fields.push({ label: getLabel(el), tag, type: el.type || null, kind: "native", filled, value });
 });

 // 2. Custom combobox (framework-agnostic)
 document.querySelectorAll("input[role=\"combobox\"][aria-autocomplete=\"list\"]").forEach(combobox => {
 if (combobox.getAttribute("aria-required") !== "true") return;

 const isInvalid = combobox.getAttribute("aria-invalid") === "true";

 // Try three methods in order to get the selected value
 const value =
 getSentinelValue(combobox) ||
 getAriaSelectedValues(combobox) ||
 getDisplayedValue(combobox) ||
 null;

 const filled = !!value && !isInvalid;

 fields.push({
 label: getLabel(combobox),
 tag: "INPUT",
 type: "combobox",
 kind: "combobox",
 id: combobox.id,
 filled,
 value
 });
 });

 // 3. Return grouped results: unfilled (needs input) and filled (for verification)
 return {
 unfilled: fields.filter(f => !f.filled),
 filled: fields.filter(f => f.filled)
 };
}