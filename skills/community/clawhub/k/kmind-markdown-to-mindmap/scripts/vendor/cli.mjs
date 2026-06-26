#!/usr/bin/env node
var __getOwnPropNames = Object.getOwnPropertyNames;
var __esm = (fn, res) => function __init() {
  return fn && (res = (0, fn[__getOwnPropNames(fn)[0]])(fn = 0)), res;
};

// ../collab/dist/broadcast-channel-sync.js
var init_broadcast_channel_sync = __esm({
  "../collab/dist/broadcast-channel-sync.js"() {
    "use strict";
  }
});

// ../collab/dist/yjs-helpers.js
var init_yjs_helpers = __esm({
  "../collab/dist/yjs-helpers.js"() {
    "use strict";
  }
});

// ../core/src/relations.ts
function normalizeRelationDirection(value) {
  return typeof value === "string" && RELATION_DIRECTIONS.has(value) ? value : void 0;
}
function normalizeRelationEndpoint(value) {
  if (!value || typeof value !== "object" || Array.isArray(value)) return null;
  const input = value;
  const kind = input.kind;
  const port = normalizeEndpointPort(input.port);
  const portRatio = normalizeEndpointPortRatio(input.portRatio);
  if (kind === "summary") {
    const summaryId = typeof input.summaryId === "string" ? input.summaryId.trim() : "";
    if (!summaryId) return null;
    return {
      kind: "summary",
      summaryId,
      ...port ? { port } : {},
      ...portRatio !== void 0 ? { portRatio } : {}
    };
  }
  const nodeId = typeof input.nodeId === "string" ? input.nodeId.trim() : "";
  if (!nodeId) return null;
  return {
    kind: "node",
    nodeId,
    ...port ? { port } : {},
    ...portRatio !== void 0 ? { portRatio } : {}
  };
}
function relationEndpointKey(endpoint) {
  return endpoint.kind === "summary" ? `summary:${endpoint.summaryId}` : `node:${endpoint.nodeId}`;
}
function relationEndpointExists(doc, endpoint) {
  return endpoint.kind === "summary" ? doc.summaries.some((summary) => summary.id === endpoint.summaryId) : Boolean(doc.nodes[endpoint.nodeId]);
}
function normalizeThemeRelationOverride(raw) {
  if (!raw || typeof raw !== "object" || Array.isArray(raw)) return void 0;
  const strokeColor = raw.strokeColor;
  const strokeWidth = raw.strokeWidth;
  const dasharray = raw.dasharray;
  const direction = normalizeRelationDirection(raw.direction);
  const next = {};
  if (typeof strokeColor === "string" && strokeColor.trim().length > 0) next.strokeColor = strokeColor.trim();
  if (typeof strokeWidth === "number" && Number.isFinite(strokeWidth)) next.strokeWidth = Math.max(0.5, Math.min(12, Math.round(strokeWidth * 10) / 10));
  if (typeof dasharray === "string" && dasharray.trim().length > 0) next.dasharray = dasharray.trim();
  if (direction) next.direction = direction;
  return Object.keys(next).length > 0 ? next : void 0;
}
function normalizeRelationForDocument(doc, relation) {
  const from = normalizeRelationEndpoint(relation.from);
  const to = normalizeRelationEndpoint(relation.to);
  if (!from || !to) return null;
  if (!relationEndpointExists(doc, from) || !relationEndpointExists(doc, to)) return null;
  if (relationEndpointKey(from) === relationEndpointKey(to)) return null;
  return {
    ...relation,
    from,
    to,
    direction: normalizeRelationDirection(relation.direction),
    style: normalizeRelationInstanceStyle(relation.style)
  };
}
function normalizeEndpointPort(value) {
  return typeof value === "string" && NODE_PORTS.has(value) ? value : void 0;
}
function normalizeEndpointPortRatio(value) {
  if (typeof value !== "number" || !Number.isFinite(value)) return void 0;
  return Math.max(0, Math.min(1, value));
}
function normalizeRelationInstanceStyle(style) {
  if (!style || typeof style !== "object") return void 0;
  const next = {};
  if (typeof style.strokeColor === "string" && style.strokeColor.trim().length > 0) next.strokeColor = style.strokeColor.trim();
  if (typeof style.strokeWidth === "number" && Number.isFinite(style.strokeWidth)) next.strokeWidth = Math.max(0.5, Math.min(12, Math.round(style.strokeWidth * 10) / 10));
  if (typeof style.strokeDasharray === "string" && style.strokeDasharray.trim().length > 0) next.strokeDasharray = style.strokeDasharray.trim();
  return Object.keys(next).length > 0 ? next : void 0;
}
var RELATION_DIRECTIONS, NODE_PORTS;
var init_relations = __esm({
  "../core/src/relations.ts"() {
    "use strict";
    RELATION_DIRECTIONS = /* @__PURE__ */ new Set(["none", "forward", "backward", "both"]);
    NODE_PORTS = /* @__PURE__ */ new Set(["top", "right", "bottom", "left"]);
  }
});

// ../core/src/theme.ts
function createDefaultThemeDefinition() {
  const baseLayout = {
    fontFamily: "ui-sans-serif, system-ui, sans-serif",
    fontSize: 14,
    fontWeight: 400,
    lineHeight: 1.4,
    textAlign: "left",
    paddingX: 12,
    paddingY: 8,
    nodeMinWidth: 60,
    nodeMinHeight: 34
  };
  const lightPaint = {
    bg: "#f8fafc",
    panel: "#ffffff",
    text: "#0f172a",
    muted: "#64748b",
    border: "#e2e8f0",
    nodeFill: "#ffffff",
    nodeFillSelected: "#eff6ff",
    nodeStroke: "#cbd5e1",
    nodeStrokeSelected: "#2563eb",
    edgeStroke: "#94a3b8",
    relationStroke: "#f59e0b",
    relationStrokeSelected: "#fb7185",
    summaryStroke: "#94a3b8"
  };
  const darkPaint = {
    bg: "#0b1220",
    panel: "#0f172a",
    text: "#e2e8f0",
    muted: "#94a3b8",
    border: "rgba(148, 163, 184, 0.25)",
    nodeFill: "#0b1220",
    nodeFillSelected: "#0b1b3a",
    nodeStroke: "rgba(148, 163, 184, 0.45)",
    nodeStrokeSelected: "#60a5fa",
    edgeStroke: "rgba(148, 163, 184, 0.55)",
    relationStroke: "#f59e0b",
    relationStrokeSelected: "#fb7185",
    summaryStroke: "rgba(148, 163, 184, 0.55)"
  };
  const baseEdges = {
    routeType: "cubic",
    strokeWidth: 2,
    cap: "round",
    join: "round"
  };
  const baseRelations = {
    strokeWidth: 2,
    cap: "round",
    join: "round"
  };
  const baseShape = {
    type: "rounded-rect",
    radius: 10,
    strokeWidth: 2
  };
  const baseRainbow = {
    enabled: false,
    palette: DEFAULT_RAINBOW_PALETTE
  };
  return {
    schemaVersion: 1,
    id: DEFAULT_THEME_ID,
    name: "KMind Default",
    variants: {
      light: {
        tokens: {
          layout: { ...baseLayout },
          paint: lightPaint
        },
        edges: baseEdges,
        relations: baseRelations,
        nodeShape: baseShape,
        rainbow: baseRainbow
      },
      dark: {
        tokens: {
          layout: { ...baseLayout },
          paint: darkPaint
        },
        edges: baseEdges,
        relations: baseRelations,
        nodeShape: baseShape,
        rainbow: baseRainbow
      }
    }
  };
}
function createDefaultDocumentThemeState(defaultTheme2) {
  return {
    schemaVersion: 1,
    defaultTheme: defaultTheme2,
    appearance: { mode: "fixed", fixed: "light" },
    rainbow: { enabled: false, branchColors: {}, paletteOverride: void 0 },
    overrides: void 0,
    rootThemes: void 0
  };
}
function resolveThemeVariantId(policy, env) {
  const fallback = "light";
  if (!policy) return fallback;
  if (policy.mode === "fixed") return policy.fixed;
  if (policy.mode === "system") return env.systemPrefersDark ? "dark" : "light";
  if (policy.mode === "external") {
    const value = env.external?.[policy.external.key];
    if (value === "dark" || value === "light") return value;
    if (typeof value === "boolean") return value ? "dark" : "light";
    return fallback;
  }
  const now = env.now ?? /* @__PURE__ */ new Date();
  const timezone = policy.time.timezone ?? "local";
  const minutes = timezone === "utc" ? now.getUTCHours() * 60 + now.getUTCMinutes() : now.getHours() * 60 + now.getMinutes();
  const lightAt = parseTimeToMinutes(policy.time.lightAt);
  const darkAt = parseTimeToMinutes(policy.time.darkAt);
  if (lightAt == null || darkAt == null) return fallback;
  if (darkAt > lightAt) {
    return minutes >= darkAt || minutes < lightAt ? "dark" : "light";
  }
  return minutes >= darkAt && minutes < lightAt ? "dark" : "light";
}
function resolveThemeDefinition(ref, assets) {
  if (ref.source === "inline") {
    return isThemeDefinition(ref.value) ? ref.value : null;
  }
  if (ref.source === "asset") {
    const asset = assets?.[ref.assetId];
    if (!asset || asset.kind !== "json") return null;
    return isThemeDefinition(asset.data) ? asset.data : null;
  }
  return null;
}
function resolveThemeVariant(definition, variantId) {
  return definition.variants[variantId] ?? definition.variants.light ?? Object.values(definition.variants)[0];
}
function ensureRainbowBranchColor(theme, branchId, palette = DEFAULT_RAINBOW_PALETTE) {
  const rainbow = theme.rainbow ?? { enabled: false, branchColors: {}, paletteOverride: void 0 };
  const branchColors = { ...rainbow.branchColors ?? {} };
  if (branchColors[branchId]) return theme;
  branchColors[branchId] = pickNextRainbowColor(branchColors, palette);
  return { ...theme, rainbow: { ...rainbow, branchColors } };
}
function pickNextRainbowColor(existing, palette) {
  const usable = palette.length > 0 ? palette : DEFAULT_RAINBOW_PALETTE;
  const used = new Set(Object.values(existing));
  for (const color of usable) {
    if (!used.has(color)) return color;
  }
  const index = Object.keys(existing).length % usable.length;
  return usable[index] ?? "#3b82f6";
}
function normalizeThemeState(raw, assets) {
  if (!raw || typeof raw !== "object" || Array.isArray(raw)) return null;
  const schemaVersion = raw.schemaVersion;
  if (schemaVersion !== 1) return null;
  const defaultTheme2 = normalizeThemeRef(raw.defaultTheme, assets);
  if (!defaultTheme2) return null;
  const rootThemesRaw = raw.rootThemes;
  const rootThemes = rootThemesRaw && typeof rootThemesRaw === "object" && !Array.isArray(rootThemesRaw) ? Object.fromEntries(
    Object.entries(rootThemesRaw).map(([id, value]) => [id, normalizeThemeRef(value, assets)]).filter((entry) => Boolean(entry[1]))
  ) : void 0;
  const rootEdgeRoutesRaw = raw.rootEdgeRoutes;
  const rootEdgeRoutes = rootEdgeRoutesRaw && typeof rootEdgeRoutesRaw === "object" && !Array.isArray(rootEdgeRoutesRaw) ? Object.fromEntries(
    Object.entries(rootEdgeRoutesRaw).filter((entry) => {
      const value = entry[1];
      return typeof value === "string" && EDGE_ROUTE_TYPES.has(value);
    })
  ) : void 0;
  const rootRainbowEdgesRaw = raw.rootRainbowEdges;
  const rootRainbowEdges = rootRainbowEdgesRaw && typeof rootRainbowEdgesRaw === "object" && !Array.isArray(rootRainbowEdgesRaw) ? Object.fromEntries(
    Object.entries(rootRainbowEdgesRaw).filter((entry) => typeof entry[1] === "boolean")
  ) : void 0;
  const edgeStyleScopesRaw = raw.edgeStyleScopes;
  const edgeStyleScopes = edgeStyleScopesRaw && typeof edgeStyleScopesRaw === "object" && !Array.isArray(edgeStyleScopesRaw) ? Object.fromEntries(
    Object.entries(edgeStyleScopesRaw).map(([id, value]) => {
      if (!value || typeof value !== "object" || Array.isArray(value)) return [id, null];
      const input = value;
      const dasharrayRaw = input.dasharray;
      const strokeWidthRaw = input.strokeWidth;
      const dasharray = typeof dasharrayRaw === "string" && dasharrayRaw.trim().length > 0 ? dasharrayRaw.trim() : void 0;
      const strokeWidth = typeof strokeWidthRaw === "number" && Number.isFinite(strokeWidthRaw) ? Math.max(0.5, Math.min(12, Math.round(strokeWidthRaw * 10) / 10)) : void 0;
      const next = {};
      if (dasharray) next.dasharray = dasharray;
      if (strokeWidth !== void 0) next.strokeWidth = strokeWidth;
      return [id, Object.keys(next).length > 0 ? next : null];
    }).filter((entry) => {
      const value = entry[1];
      if (!value) return false;
      return Object.keys(value).length > 0;
    })
  ) : void 0;
  const relationStyle = normalizeThemeRelationOverride(raw.relationStyle);
  const rootRelationStylesRaw = raw.rootRelationStyles;
  const rootRelationStyles = rootRelationStylesRaw && typeof rootRelationStylesRaw === "object" && !Array.isArray(rootRelationStylesRaw) ? Object.fromEntries(
    Object.entries(rootRelationStylesRaw).map(([id, value]) => [id, normalizeThemeRelationOverride(value)]).filter((entry) => Boolean(entry[1]))
  ) : void 0;
  const rainbowRaw = raw.rainbow;
  const rainbow = rainbowRaw && typeof rainbowRaw === "object" && !Array.isArray(rainbowRaw) ? normalizeRainbowState(rainbowRaw) : void 0;
  const appearance = normalizeAppearancePolicy(raw.appearance);
  const overridesRaw = raw.overrides;
  const overrides = overridesRaw && typeof overridesRaw === "object" && !Array.isArray(overridesRaw) ? normalizeOverrides(overridesRaw) : void 0;
  return {
    schemaVersion: 1,
    defaultTheme: defaultTheme2,
    rootThemes: rootThemes && Object.keys(rootThemes).length > 0 ? rootThemes : void 0,
    rootEdgeRoutes: rootEdgeRoutes && Object.keys(rootEdgeRoutes).length > 0 ? rootEdgeRoutes : void 0,
    rootRainbowEdges: rootRainbowEdges && Object.keys(rootRainbowEdges).length > 0 ? rootRainbowEdges : void 0,
    edgeStyleScopes: edgeStyleScopes && Object.keys(edgeStyleScopes).length > 0 ? edgeStyleScopes : void 0,
    relationStyle,
    rootRelationStyles: rootRelationStyles && Object.keys(rootRelationStyles).length > 0 ? rootRelationStyles : void 0,
    rainbow,
    appearance,
    overrides
  };
}
function parseTimeToMinutes(value) {
  if (typeof value !== "string") return null;
  const match = value.trim().match(/^(\d{1,2}):(\d{2})$/);
  if (!match) return null;
  const hours = Number(match[1]);
  const minutes = Number(match[2]);
  if (!Number.isFinite(hours) || !Number.isFinite(minutes)) return null;
  if (hours < 0 || hours > 23) return null;
  if (minutes < 0 || minutes > 59) return null;
  return hours * 60 + minutes;
}
function normalizeThemeRef(raw, assets) {
  if (!raw || typeof raw !== "object" || Array.isArray(raw)) return null;
  const source = raw.source;
  if (source === "inline") {
    const value = raw.value;
    if (isThemeDefinition(value)) return { source: "inline", value };
    return null;
  }
  if (source === "asset") {
    const assetId = raw.assetId;
    if (typeof assetId !== "string") return null;
    const asset = assets[assetId];
    if (asset && asset.kind === "json" && isThemeDefinition(asset.data)) {
      return { source: "asset", assetId };
    }
    return { source: "asset", assetId };
  }
  if (source === "remote") {
    const themeId = raw.themeId;
    const version = raw.version;
    if (typeof themeId !== "string" || themeId.length === 0) return null;
    return { source: "remote", themeId, version: typeof version === "string" ? version : void 0 };
  }
  return null;
}
function normalizeAppearancePolicy(raw) {
  if (!raw || typeof raw !== "object" || Array.isArray(raw)) return void 0;
  const mode = raw.mode;
  if (mode === "fixed") {
    const fixed = raw.fixed;
    if (fixed === "dark" || fixed === "light") return { mode: "fixed", fixed };
    return void 0;
  }
  if (mode === "system") return { mode: "system" };
  if (mode === "time") {
    const time = raw.time;
    if (!time || typeof time !== "object" || Array.isArray(time)) return void 0;
    const lightAt = time.lightAt;
    const darkAt = time.darkAt;
    const timezone = time.timezone;
    if (typeof lightAt !== "string" || typeof darkAt !== "string") return void 0;
    return {
      mode: "time",
      time: {
        lightAt,
        darkAt,
        timezone: timezone === "utc" ? "utc" : "local"
      }
    };
  }
  if (mode === "external") {
    const external = raw.external;
    if (!external || typeof external !== "object" || Array.isArray(external)) return void 0;
    const key = external.key;
    if (typeof key !== "string" || key.length === 0) return void 0;
    return { mode: "external", external: { key } };
  }
  return void 0;
}
function normalizeRainbowState(raw) {
  const enabled = Boolean(raw.enabled);
  const branchColors = normalizeStringRecord(raw.branchColors);
  const paletteOverride = normalizeStringArray(raw.paletteOverride);
  return {
    enabled,
    branchColors,
    paletteOverride
  };
}
function normalizeOverrides(raw) {
  const nodesRaw = raw.nodes;
  const edgesRaw = raw.edges;
  const relationsRaw = raw.relations;
  const summariesRaw = raw.summaries;
  const nodes = nodesRaw && typeof nodesRaw === "object" && !Array.isArray(nodesRaw) ? normalizeRecord(nodesRaw, normalizeNodeStylePatch) : void 0;
  const edges = edgesRaw && typeof edgesRaw === "object" && !Array.isArray(edgesRaw) ? normalizeRecord(edgesRaw, normalizeEdgeOverride) : void 0;
  const relations = relationsRaw && typeof relationsRaw === "object" && !Array.isArray(relationsRaw) ? normalizeRecord(relationsRaw, normalizeRelationOverride) : void 0;
  const summaries = summariesRaw && typeof summariesRaw === "object" && !Array.isArray(summariesRaw) ? normalizeRecord(summariesRaw, normalizeSummaryOverride) : void 0;
  if (!nodes && !edges && !relations && !summaries) return void 0;
  return {
    nodes,
    edges,
    relations,
    summaries
  };
}
function normalizeNodeStylePatch(raw) {
  if (!raw || typeof raw !== "object" || Array.isArray(raw)) return void 0;
  const layout = normalizeObject(raw, "layout");
  const paint = normalizeObject(raw, "paint");
  const nodeShape = normalizeObject(raw, "nodeShape");
  const incomingEdge = normalizeObject(raw, "incomingEdge");
  const patch = {};
  if (layout) patch.layout = layout;
  if (paint) patch.paint = paint;
  if (nodeShape) patch.nodeShape = nodeShape;
  if (incomingEdge) patch.incomingEdge = incomingEdge;
  return Object.keys(patch).length > 0 ? patch : void 0;
}
function normalizeEdgeOverride(raw) {
  if (!raw || typeof raw !== "object" || Array.isArray(raw)) return void 0;
  const strokeColor = raw.strokeColor;
  const strokeWidth = raw.strokeWidth;
  const dasharray = raw.dasharray;
  const next = {};
  if (typeof strokeColor === "string") next.strokeColor = strokeColor;
  if (typeof strokeWidth === "number" && Number.isFinite(strokeWidth)) next.strokeWidth = strokeWidth;
  if (typeof dasharray === "string") next.dasharray = dasharray;
  return Object.keys(next).length > 0 ? next : void 0;
}
function normalizeRelationOverride(raw) {
  return normalizeThemeRelationOverride(raw);
}
function normalizeSummaryOverride(raw) {
  if (!raw || typeof raw !== "object" || Array.isArray(raw)) return void 0;
  const strokeColor = raw.strokeColor;
  const fill = raw.fill;
  const textColor = raw.textColor;
  const next = {};
  if (typeof strokeColor === "string") next.strokeColor = strokeColor;
  if (typeof fill === "string") next.fill = fill;
  if (typeof textColor === "string") next.textColor = textColor;
  return Object.keys(next).length > 0 ? next : void 0;
}
function normalizeObject(raw, key) {
  const value = raw && typeof raw === "object" && !Array.isArray(raw) ? raw[key] : void 0;
  if (!value || typeof value !== "object" || Array.isArray(value)) return void 0;
  return value;
}
function normalizeStringRecord(raw) {
  if (!raw || typeof raw !== "object" || Array.isArray(raw)) return void 0;
  const result2 = {};
  for (const [key, value] of Object.entries(raw)) {
    if (typeof value !== "string") continue;
    result2[key] = value;
  }
  return Object.keys(result2).length > 0 ? result2 : void 0;
}
function normalizeStringArray(raw) {
  if (!Array.isArray(raw)) return void 0;
  const result2 = raw.filter((item) => typeof item === "string");
  return result2.length > 0 ? result2 : void 0;
}
function normalizeRecord(raw, normalizeValue) {
  const next = {};
  for (const [key, value] of Object.entries(raw)) {
    const normalized = normalizeValue(value);
    if (!normalized) continue;
    next[key] = normalized;
  }
  return Object.keys(next).length > 0 ? next : void 0;
}
function isThemeDefinition(raw) {
  if (!raw || typeof raw !== "object" || Array.isArray(raw)) return false;
  if (raw.schemaVersion !== 1) return false;
  if (typeof raw.id !== "string") return false;
  if (typeof raw.name !== "string") return false;
  const variants = raw.variants;
  if (!variants || typeof variants !== "object" || Array.isArray(variants)) return false;
  return true;
}
var DEFAULT_THEME_ID, EDGE_ROUTE_TYPES, DEFAULT_RAINBOW_PALETTE;
var init_theme = __esm({
  "../core/src/theme.ts"() {
    "use strict";
    init_relations();
    DEFAULT_THEME_ID = "kmind-default";
    EDGE_ROUTE_TYPES = /* @__PURE__ */ new Set([
      "cubic",
      "quadratic",
      "straight",
      "orthogonal",
      "orthogonal-rounded",
      "tapered",
      "center-quadratic",
      "center-quadratic-tapered",
      "edge-lead-quadratic",
      "edge-lead-quadratic-tapered",
      "cubic-tail",
      "baseline-fork"
    ]);
    DEFAULT_RAINBOW_PALETTE = [
      "#ef4444",
      "#f97316",
      "#eab308",
      "#22c55e",
      "#06b6d4",
      "#3b82f6",
      "#8b5cf6",
      "#ec4899"
    ];
  }
});

// ../core/src/root-positions.ts
function seedMissingRootPositions(args) {
  const { roots } = args;
  const existing = args.existing ?? {};
  const baseX = roots.map((id) => existing[id]).find((pos) => Boolean(pos))?.x ?? DEFAULT_ROOT_POSITION.x;
  const next = {};
  let lastY = null;
  for (const rootId of roots) {
    const current = existing[rootId];
    if (current) {
      next[rootId] = current;
      lastY = current.y;
      continue;
    }
    const y = lastY === null ? DEFAULT_ROOT_POSITION.y : lastY + DEFAULT_ROOT_GAP_Y;
    next[rootId] = { x: baseX, y };
    lastY = y;
  }
  return next;
}
var DEFAULT_ROOT_POSITION, DEFAULT_ROOT_GAP_Y;
var init_root_positions = __esm({
  "../core/src/root-positions.ts"() {
    "use strict";
    DEFAULT_ROOT_POSITION = { x: 120, y: 60 };
    DEFAULT_ROOT_GAP_Y = 260;
  }
});

// ../core/src/pos.ts
function assertValidPos(pos) {
  if (pos.length === 0) throw new Error("Invalid pos: empty string.");
  for (let i = 0; i < pos.length; i += 1) {
    const ch = pos[i];
    if (POS_INDEX[ch] === void 0) throw new Error(`Invalid pos: contains unsupported char "${ch}".`);
  }
}
function comparePos(a, b) {
  if (a === b) return 0;
  return a < b ? -1 : 1;
}
function posBefore(pos) {
  assertValidPos(pos);
  const chars = pos.split("");
  for (let i = chars.length - 1; i >= 0; i -= 1) {
    const ch = chars[i];
    const idx = POS_INDEX[ch];
    if (idx === 0) continue;
    chars[i] = POS_ALPHABET[idx - 1];
    for (let j = i + 1; j < chars.length; j += 1) chars[j] = POS_MAX_CHAR;
    return chars.join("");
  }
  throw new Error("posBefore: cannot generate a key before the minimal pos.");
}
function posAfter(pos) {
  assertValidPos(pos);
  const last = pos[pos.length - 1];
  const idx = POS_INDEX[last];
  if (idx < POS_BASE - 1) {
    return `${pos.slice(0, -1)}${POS_ALPHABET[idx + 1]}`;
  }
  return `${pos}${POS_MID_CHAR}`;
}
function posBetweenFinite(left, right) {
  assertValidPos(left);
  assertValidPos(right);
  if (comparePos(left, right) >= 0) {
    throw new Error("posBetween: left must be < right.");
  }
  let prefix = "";
  let i = 0;
  while (true) {
    const lch = i < left.length ? left[i] : POS_MIN_CHAR;
    const rch = i < right.length ? right[i] : POS_MAX_CHAR;
    if (lch === rch) {
      prefix += lch;
      i += 1;
      continue;
    }
    const li = POS_INDEX[lch];
    const ri = POS_INDEX[rch];
    if (li === void 0 || ri === void 0) {
      throw new Error("posBetween: invalid input pos.");
    }
    if (ri - li > 1) {
      const mid = Math.ceil((li + ri) / 2);
      return `${prefix}${POS_ALPHABET[mid]}`;
    }
    prefix += lch;
    i += 1;
  }
}
function posBetween(left, right) {
  if (!left && !right) return "a0";
  if (!left && right) return posBefore(right);
  if (left && !right) return posAfter(left);
  return posBetweenFinite(left, right);
}
function pow(base, exp) {
  let acc = 1;
  for (let i = 0; i < exp; i += 1) acc *= base;
  return acc;
}
function encodeIndexFixedWidth(index, width) {
  let value = Math.max(0, Math.floor(index));
  const chars = new Array(width).fill(POS_MIN_CHAR);
  for (let i = width - 1; i >= 0; i -= 1) {
    chars[i] = POS_ALPHABET[value % POS_BASE];
    value = Math.floor(value / POS_BASE);
  }
  return chars.join("");
}
function renormalizePosList(count) {
  const n = Math.max(0, Math.floor(count));
  if (n === 0) return [];
  if (n === 1) return ["a0"];
  let width = 2;
  while (pow(POS_BASE, width) < n + 2) width += 1;
  const maxIndex = pow(POS_BASE, width) - 1;
  const start = Math.floor((maxIndex - (n - 1)) / 2);
  const result2 = [];
  for (let i = 0; i < n; i += 1) {
    result2.push(encodeIndexFixedWidth(start + i, width));
  }
  return result2;
}
var POS_ALPHABET, POS_BASE, POS_MIN_CHAR, POS_MAX_CHAR, POS_MID_CHAR, POS_INDEX;
var init_pos = __esm({
  "../core/src/pos.ts"() {
    "use strict";
    POS_ALPHABET = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz";
    POS_BASE = POS_ALPHABET.length;
    POS_MIN_CHAR = POS_ALPHABET[0];
    POS_MAX_CHAR = POS_ALPHABET[POS_BASE - 1];
    POS_MID_CHAR = POS_ALPHABET[Math.ceil((0 + (POS_BASE - 1)) / 2)];
    POS_INDEX = Object.fromEntries(
      POS_ALPHABET.split("").map((ch, index) => [ch, index])
    );
  }
});

// ../core/src/node-content-width.ts
function isFinitePositiveNumber(value) {
  return typeof value === "number" && Number.isFinite(value) && value > 0;
}
function normalizeWidth(value) {
  return Math.round(value);
}
function normalizeOptionalWidth(value) {
  return isFinitePositiveNumber(value) ? normalizeWidth(value) : void 0;
}
function normalizeNodeContentWidth(contentWidth) {
  if (!contentWidth || typeof contentWidth !== "object" || Array.isArray(contentWidth)) return void 0;
  if (contentWidth.mode === "fixed") {
    const nextWidth = normalizeWidth(isFinitePositiveNumber(contentWidth.width) ? contentWidth.width : DEFAULT_NODE_CONTENT_WRAP_WIDTH);
    const restoreAutoWrapWidth = normalizeOptionalWidth(contentWidth.restoreAutoWrapWidth);
    return restoreAutoWrapWidth !== void 0 ? { mode: "fixed", width: nextWidth, restoreAutoWrapWidth } : { mode: "fixed", width: nextWidth };
  }
  if (contentWidth.mode === "auto") {
    return isFinitePositiveNumber(contentWidth.wrapWidth) ? { mode: "auto", wrapWidth: normalizeWidth(contentWidth.wrapWidth) } : { mode: "auto" };
  }
  return void 0;
}
function mirrorLegacyNodeContentWidth(contentWidth) {
  const normalized = normalizeNodeContentWidth(contentWidth);
  if (!normalized) return {};
  if (normalized.mode === "fixed") {
    return { maxWidth: normalized.width, contentWidthMode: "fixed" };
  }
  if (isFinitePositiveNumber(normalized.wrapWidth)) {
    return { maxWidth: normalized.wrapWidth, contentWidthMode: "auto" };
  }
  return {};
}
function resolveNodeAutoContentWidth(node) {
  const normalized = normalizeNodeContentWidth(node?.contentWidth);
  if (normalized?.mode === "auto") return normalized;
  if (normalized?.mode === "fixed") {
    return normalized.restoreAutoWrapWidth !== void 0 ? { mode: "auto", wrapWidth: normalized.restoreAutoWrapWidth } : { mode: "auto" };
  }
  const legacyWidth = normalizeOptionalWidth(node?.maxWidth);
  if (node?.contentWidthMode === "fixed") return { mode: "auto" };
  if (legacyWidth !== void 0) return { mode: "auto", wrapWidth: legacyWidth };
  return { mode: "auto" };
}
function resolveNodeFixedContentWidth(node, width, options) {
  const normalizedWidth = normalizeWidth(isFinitePositiveNumber(width) ? width : DEFAULT_NODE_CONTENT_WRAP_WIDTH);
  const preservedAutoWrapWidth = normalizeOptionalWidth(options?.restoreAutoWrapWidth) ?? normalizeOptionalWidth(resolveNodeAutoContentWidth(node).wrapWidth);
  return preservedAutoWrapWidth !== void 0 ? { mode: "fixed", width: normalizedWidth, restoreAutoWrapWidth: preservedAutoWrapWidth } : { mode: "fixed", width: normalizedWidth };
}
function applyNodeContentWidth(node, contentWidth) {
  const normalized = normalizeNodeContentWidth(contentWidth);
  const legacy = mirrorLegacyNodeContentWidth(normalized);
  return {
    ...node,
    contentWidth: normalized,
    maxWidth: legacy.maxWidth,
    contentWidthMode: legacy.contentWidthMode
  };
}
function resolveNodeContentWidth(node, options) {
  const defaultWrapWidth = isFinitePositiveNumber(options?.defaultWrapWidth) ? normalizeWidth(options.defaultWrapWidth) : DEFAULT_NODE_CONTENT_WRAP_WIDTH;
  const normalized = normalizeNodeContentWidth(node?.contentWidth);
  if (normalized) {
    if (normalized.mode === "fixed") return normalized;
    return {
      mode: "auto",
      wrapWidth: normalized.wrapWidth,
      width: isFinitePositiveNumber(normalized.wrapWidth) ? normalized.wrapWidth : defaultWrapWidth
    };
  }
  const legacyWidth = isFinitePositiveNumber(node?.maxWidth) ? normalizeWidth(node.maxWidth) : void 0;
  if (node?.contentWidthMode === "fixed") {
    return { mode: "fixed", width: legacyWidth ?? defaultWrapWidth };
  }
  return {
    mode: "auto",
    wrapWidth: legacyWidth,
    width: legacyWidth ?? defaultWrapWidth
  };
}
var DEFAULT_NODE_CONTENT_WRAP_WIDTH;
var init_node_content_width = __esm({
  "../core/src/node-content-width.ts"() {
    "use strict";
    DEFAULT_NODE_CONTENT_WRAP_WIDTH = 240;
  }
});

// ../core/src/document.ts
function createNode(id, options = {}) {
  const contentWidth = options.contentWidth ?? (options.contentWidthMode === "fixed" ? { mode: "fixed", width: options.maxWidth ?? 240 } : typeof options.maxWidth === "number" ? { mode: "auto", wrapWidth: options.maxWidth } : void 0);
  return applyNodeContentWidth({
    id,
    parentId: options.parentId,
    parentSummaryId: options.parentSummaryId,
    pos: options.pos,
    children: options.children ?? [],
    text: options.text ?? "",
    content: options.content,
    attrs: options.attrs,
    subMapId: options.subMapId,
    data: options.data,
    contentWidth: options.contentWidth,
    maxWidth: options.maxWidth,
    contentWidthMode: options.contentWidthMode,
    layout: options.layout,
    branchSide: options.branchSide
  }, contentWidth);
}
function createDocument(idGenerator, options = {}) {
  const rootId = idGenerator.generate("node");
  const rootNode = createNode(rootId, {
    text: options.rootText ?? "Root",
    contentWidth: { mode: "auto", wrapWidth: options.rootMaxWidth ?? 240 },
    pos: posBetween(null, null)
  });
  return {
    version: "1.0.0",
    roots: [rootId],
    rootPositions: {
      [rootId]: { ...DEFAULT_ROOT_POSITION }
    },
    nodes: {
      [rootId]: rootNode
    },
    summaries: [],
    relations: [],
    assets: {},
    theme: createDefaultDocumentThemeState({
      source: "inline",
      value: createDefaultThemeDefinition()
    })
  };
}
var init_document = __esm({
  "../core/src/document.ts"() {
    "use strict";
    init_theme();
    init_root_positions();
    init_pos();
    init_node_content_width();
  }
});

// ../core/src/summaries.ts
function buildSummariesByParent(doc) {
  const map = /* @__PURE__ */ new Map();
  for (const summary of doc.summaries) {
    const list = map.get(summary.parentId);
    if (list) {
      list.push(summary);
    } else {
      map.set(summary.parentId, [summary]);
    }
  }
  return map;
}
function collectSubtreeIds(doc, nodeId, summariesByParent) {
  const summaryById = new Map(doc.summaries.map((summary) => [summary.id, summary]));
  const stack = [nodeId];
  const visited = /* @__PURE__ */ new Set();
  const result2 = [];
  while (stack.length > 0) {
    const current = stack.pop();
    if (!current) break;
    if (visited.has(current)) continue;
    visited.add(current);
    const node = doc.nodes[current];
    if (node) {
      result2.push(current);
      for (const childId of node.children) {
        stack.push(childId);
      }
    }
    const summaries = summariesByParent.get(current);
    if (summaries) {
      for (const summary2 of summaries) {
        stack.push(summary2.id);
        for (const childId of summary2.children) {
          stack.push(childId);
        }
      }
    }
    const summary = summaryById.get(current);
    if (summary) {
      for (const childId of summary.children) {
        stack.push(childId);
      }
    }
  }
  return result2;
}
function sanitizeSummaries(args) {
  const nextNodes = { ...args.nodes };
  let nextRoots = [...args.roots];
  const originalById = new Map(args.originalSummaries.map((summary) => [summary.id, summary]));
  const summaryById = /* @__PURE__ */ new Map();
  for (const summary of args.summaries) {
    summaryById.set(summary.id, { ...summary, childIds: [...summary.childIds], children: [...summary.children] });
  }
  const resolvePromotionTarget = (parentId) => {
    let cursor = parentId;
    const visited = /* @__PURE__ */ new Set();
    while (cursor) {
      if (visited.has(cursor)) break;
      visited.add(cursor);
      if (nextNodes[cursor]) return { type: "node", id: cursor };
      if (summaryById.has(cursor)) return { type: "summary", id: cursor };
      const originalParent = originalById.get(cursor);
      if (!originalParent) break;
      cursor = originalParent.parentId;
    }
    return { type: "root" };
  };
  const resolveParentKind = (parentId) => {
    if (nextNodes[parentId]) return "node";
    if (summaryById.has(parentId) || originalById.has(parentId)) return "summary";
    return "missing";
  };
  const attachToTarget = (nodeId, target) => {
    const node = nextNodes[nodeId];
    if (!node) return;
    if (target.type === "root") {
      const baseRoots = nextRoots.filter((id) => id !== nodeId);
      const lastRootId = baseRoots[baseRoots.length - 1] ?? null;
      const lastPos2 = lastRootId ? nextNodes[lastRootId]?.pos ?? null : null;
      const nextPos2 = lastPos2 ? posBetween(lastPos2, null) : posBetween(null, null);
      nextNodes[nodeId] = { ...node, parentId: void 0, parentSummaryId: void 0, pos: nextPos2 };
      nextRoots = [...baseRoots, nodeId];
      return;
    }
    if (target.type === "node") {
      const parent = nextNodes[target.id];
      if (!parent) return;
      const baseChildren2 = parent.children.filter((id) => id !== nodeId);
      const lastSiblingId2 = baseChildren2[baseChildren2.length - 1] ?? null;
      const lastPos2 = lastSiblingId2 ? nextNodes[lastSiblingId2]?.pos ?? null : null;
      const nextPos2 = lastPos2 ? posBetween(lastPos2, null) : posBetween(null, null);
      nextNodes[nodeId] = { ...node, parentId: target.id, parentSummaryId: void 0, pos: nextPos2 };
      nextNodes[target.id] = { ...parent, children: [...baseChildren2, nodeId] };
      return;
    }
    const parentSummary = summaryById.get(target.id);
    if (!parentSummary) {
      const baseRoots = nextRoots.filter((id) => id !== nodeId);
      const lastRootId = baseRoots[baseRoots.length - 1] ?? null;
      const lastPos2 = lastRootId ? nextNodes[lastRootId]?.pos ?? null : null;
      const nextPos2 = lastPos2 ? posBetween(lastPos2, null) : posBetween(null, null);
      nextNodes[nodeId] = { ...node, parentId: void 0, parentSummaryId: void 0, pos: nextPos2 };
      nextRoots = [...baseRoots, nodeId];
      return;
    }
    const baseChildren = parentSummary.children.filter((id) => id !== nodeId);
    const lastSiblingId = baseChildren[baseChildren.length - 1] ?? null;
    const lastPos = lastSiblingId ? nextNodes[lastSiblingId]?.pos ?? null : null;
    const nextPos = lastPos ? posBetween(lastPos, null) : posBetween(null, null);
    nextNodes[nodeId] = { ...node, parentId: void 0, parentSummaryId: target.id, pos: nextPos };
    summaryById.set(target.id, { ...parentSummary, children: [...baseChildren, nodeId] });
  };
  const normalizeSummaries = () => {
    for (const summary of summaryById.values()) {
      const parentKind = resolveParentKind(summary.parentId);
      summary.childIds = summary.childIds.filter((id) => {
        const child = nextNodes[id];
        if (!child) return false;
        if (parentKind === "node") return child.parentId === summary.parentId;
        if (parentKind === "summary") return child.parentSummaryId === summary.parentId;
        return false;
      });
      if (summary.childIds.length > 0) {
        const containerChildIds = (() => {
          if (parentKind === "node") {
            const parent = nextNodes[summary.parentId];
            if (!parent) return [];
            const resolveSide = (nodeId) => nextNodes[nodeId]?.branchSide === "left" ? "left" : "right";
            const validChildren = parent.children.filter((id) => {
              const child = nextNodes[id];
              if (!child) return false;
              return child.parentId === parent.id;
            });
            const layoutType = parent.layout ?? "logical-right";
            if (layoutType !== "mindmap-both" && layoutType !== "mindmap-both-auto") return validChildren;
            const selectedSides = new Set(summary.childIds.map((id) => resolveSide(id)));
            if (selectedSides.size !== 1) return validChildren;
            const targetSide = selectedSides.has("left") ? "left" : "right";
            return validChildren.filter((id) => resolveSide(id) === targetSide);
          }
          if (parentKind === "summary") {
            const parentSummary = summaryById.get(summary.parentId);
            return parentSummary ? parentSummary.children.filter((id) => {
              const child = nextNodes[id];
              if (!child) return false;
              return child.parentSummaryId === parentSummary.id;
            }) : [];
          }
          return [];
        })();
        const indexById = new Map(containerChildIds.map((id, index) => [id, index]));
        const startId = summary.childIds[0];
        const endId = summary.childIds[summary.childIds.length - 1];
        const startIndex = indexById.get(startId);
        const endIndex = indexById.get(endId);
        if (startIndex !== void 0 && endIndex !== void 0) {
          const rangeStart = Math.min(startIndex, endIndex);
          const rangeEnd = Math.max(startIndex, endIndex);
          summary.childIds = containerChildIds.slice(rangeStart, rangeEnd + 1);
        } else {
          const indices = summary.childIds.map((id) => indexById.get(id)).filter((index) => index !== void 0);
          if (indices.length > 0) {
            const rangeStart = Math.min(...indices);
            const rangeEnd = Math.max(...indices);
            summary.childIds = containerChildIds.slice(rangeStart, rangeEnd + 1);
          }
        }
      }
      summary.children = summary.children.filter((id) => {
        const child = nextNodes[id];
        if (!child) return false;
        return child.parentSummaryId === summary.id;
      });
    }
  };
  normalizeSummaries();
  let changed = true;
  while (changed) {
    changed = false;
    for (const summary of Array.from(summaryById.values())) {
      const parentExists = Boolean(nextNodes[summary.parentId]) || summaryById.has(summary.parentId);
      if (parentExists && summary.childIds.length > 0) continue;
      const target = resolvePromotionTarget(summary.parentId);
      for (const childId of summary.children) {
        attachToTarget(childId, target);
      }
      summaryById.delete(summary.id);
      changed = true;
    }
    if (changed) normalizeSummaries();
  }
  nextRoots = Array.from(new Set(nextRoots)).filter((id) => Boolean(nextNodes[id]));
  nextRoots = nextRoots.filter((id) => {
    const node = nextNodes[id];
    if (!node) return false;
    return !node.parentId && !node.parentSummaryId;
  });
  return {
    nodes: pruneDanglingChildren(nextNodes),
    roots: nextRoots,
    summaries: Array.from(summaryById.values())
  };
}
function pruneDanglingChildren(nodes) {
  const next = {};
  for (const [id, node] of Object.entries(nodes)) {
    next[id] = { ...node, children: node.children.filter((childId) => Boolean(nodes[childId])) };
  }
  return next;
}
var init_summaries = __esm({
  "../core/src/summaries.ts"() {
    "use strict";
    init_pos();
  }
});

// ../core/src/tree.ts
function resolveParentKey(args) {
  const parentId = args.node.parentId;
  if (parentId && args.nodes[parentId]) return { key: `node:${parentId}`, normalizedParent: { parentId } };
  const parentSummaryId = args.node.parentSummaryId;
  if (parentSummaryId && args.summaryIdSet.has(parentSummaryId)) {
    return { key: `summary:${parentSummaryId}`, normalizedParent: { parentSummaryId } };
  }
  return { key: "root", normalizedParent: { parentId: void 0, parentSummaryId: void 0 } };
}
function comparePosThenId(a, b) {
  const ap = a.pos;
  const bp = b.pos;
  if (ap && bp && ap !== bp) return comparePos(ap, bp);
  if (!ap && bp) return 1;
  if (ap && !bp) return -1;
  return a.id.localeCompare(b.id);
}
function getHintOrder(args) {
  if (args.parentKey === "root") return Array.isArray(args.doc.roots) ? args.doc.roots : [];
  if (args.parentKey.startsWith("node:")) {
    const parentId = args.parentKey.slice("node:".length);
    const parent = args.doc.nodes[parentId];
    return parent ? parent.children : [];
  }
  const summaryId = args.parentKey.slice("summary:".length);
  const summary = args.summariesById.get(summaryId);
  return summary ? summary.children : [];
}
function getNodePos(node) {
  const raw = typeof node.pos === "string" ? node.pos.trim() : "";
  return raw.length > 0 ? raw : null;
}
function normalizeTree(doc) {
  const summariesById = /* @__PURE__ */ new Map();
  for (const summary of doc.summaries) summariesById.set(summary.id, summary);
  const summaryIdSet = new Set(summariesById.keys());
  const nextNodes = { ...doc.nodes };
  let posChanged = false;
  let parentChanged = false;
  const idsByParent = /* @__PURE__ */ new Map();
  for (const [id, rawNode] of Object.entries(doc.nodes)) {
    const { key, normalizedParent } = resolveParentKey({ node: rawNode, nodes: doc.nodes, summaryIdSet });
    const list = idsByParent.get(key) ?? [];
    list.push(id);
    idsByParent.set(key, list);
    const wantsParentId = normalizedParent.parentId;
    const wantsParentSummaryId = normalizedParent.parentSummaryId;
    if (rawNode.parentId !== wantsParentId || rawNode.parentSummaryId !== wantsParentSummaryId) {
      parentChanged = true;
      nextNodes[id] = { ...rawNode, parentId: wantsParentId, parentSummaryId: wantsParentSummaryId };
    }
  }
  for (const [parentKey, childIds] of idsByParent.entries()) {
    if (childIds.length <= 1) {
      const id = childIds[0];
      if (!id) continue;
      const node = nextNodes[id];
      if (!node) continue;
      if (!getNodePos(node)) {
        posChanged = true;
        nextNodes[id] = { ...node, pos: posBetween(null, null) };
      }
      continue;
    }
    const hint = getHintOrder({ parentKey, doc, summariesById });
    const childIdSet = new Set(childIds);
    const used = /* @__PURE__ */ new Set();
    const ordered = [];
    for (const id of hint) {
      if (!childIdSet.has(id)) continue;
      if (used.has(id)) continue;
      ordered.push(id);
      used.add(id);
    }
    const remaining = childIds.filter((id) => !used.has(id)).map((id) => ({ id, pos: nextNodes[id] ? getNodePos(nextNodes[id]) : null })).sort(comparePosThenId).map((item) => item.id);
    ordered.push(...remaining);
    const needsRenormalize = childIds.some((id) => {
      const node = nextNodes[id];
      return !node || !getNodePos(node);
    });
    if (!needsRenormalize) continue;
    const positions = renormalizePosList(ordered.length);
    for (let i = 0; i < ordered.length; i += 1) {
      const id = ordered[i];
      const node = nextNodes[id];
      if (!node) continue;
      const nextPos = positions[i] ?? posBetween(null, null);
      if (node.pos === nextPos) continue;
      posChanged = true;
      nextNodes[id] = { ...node, pos: nextPos };
    }
  }
  const itemsByParent = /* @__PURE__ */ new Map();
  for (const [id, rawNode] of Object.entries(nextNodes)) {
    const { key } = resolveParentKey({ node: rawNode, nodes: nextNodes, summaryIdSet });
    const list = itemsByParent.get(key) ?? [];
    list.push({ id, pos: getNodePos(rawNode) });
    itemsByParent.set(key, list);
  }
  const normalizedNodes = {};
  for (const [id, node] of Object.entries(nextNodes)) {
    normalizedNodes[id] = { ...node, children: [] };
  }
  const normalizedSummaries = doc.summaries.map((summary) => ({ ...summary, children: [] }));
  const normalizedSummariesById = new Map(normalizedSummaries.map((summary) => [summary.id, summary]));
  const roots = [];
  for (const [parentKey, items] of itemsByParent.entries()) {
    const ordered = [...items].sort(comparePosThenId).map((item) => item.id);
    if (parentKey === "root") {
      roots.push(...ordered);
      continue;
    }
    if (parentKey.startsWith("node:")) {
      const parentId = parentKey.slice("node:".length);
      const parent = normalizedNodes[parentId];
      if (parent) normalizedNodes[parentId] = { ...parent, children: ordered };
      continue;
    }
    const summaryId = parentKey.slice("summary:".length);
    const summary = normalizedSummariesById.get(summaryId);
    if (summary) normalizedSummariesById.set(summaryId, { ...summary, children: ordered });
  }
  const treeChanged = parentChanged || posChanged;
  if (!treeChanged) {
    return { ...doc, roots, nodes: normalizedNodes, summaries: Array.from(normalizedSummariesById.values()) };
  }
  return { ...doc, roots, nodes: normalizedNodes, summaries: Array.from(normalizedSummariesById.values()) };
}
var init_tree = __esm({
  "../core/src/tree.ts"() {
    "use strict";
    init_pos();
  }
});

// ../core/src/commands.ts
function pruneDanglingInternalLinks(nodes, deletedNodeIds) {
  let changed = false;
  const nextNodes = { ...nodes };
  for (const [nodeId, node] of Object.entries(nodes)) {
    const content = node.content;
    if (!content || content.schemaVersion !== 1) continue;
    if (content.kind !== "blocks") continue;
    let blocksChanged = false;
    const nextBlocks = content.blocks.map((block) => {
      if (block.type !== "links") return block;
      const nextLinks = block.links.filter((link) => {
        if (link.kind !== "internal") return true;
        const normalizedDocId = typeof link.docId === "string" ? link.docId.trim() : "";
        if (normalizedDocId.length > 0) return true;
        return !deletedNodeIds.has(link.nodeId);
      });
      if (nextLinks.length === block.links.length) return block;
      blocksChanged = true;
      return { ...block, links: nextLinks };
    });
    if (!blocksChanged) continue;
    changed = true;
    nextNodes[nodeId] = { ...node, content: { ...content, blocks: nextBlocks } };
  }
  return changed ? nextNodes : nodes;
}
function pruneDanglingInternalLinksInSummaries(summaries, deletedNodeIds) {
  let changed = false;
  const next = summaries.map((summary) => {
    const content = summary.content;
    if (!content || content.schemaVersion !== 1) return summary;
    if (content.kind !== "blocks") return summary;
    let blocksChanged = false;
    const nextBlocks = content.blocks.map((block) => {
      if (block.type !== "links") return block;
      const nextLinks = block.links.filter((link) => {
        if (link.kind !== "internal") return true;
        const normalizedDocId = typeof link.docId === "string" ? link.docId.trim() : "";
        if (normalizedDocId.length > 0) return true;
        return !deletedNodeIds.has(link.nodeId);
      });
      if (nextLinks.length === block.links.length) return block;
      blocksChanged = true;
      return { ...block, links: nextLinks };
    });
    if (!blocksChanged) return summary;
    changed = true;
    return { ...summary, content: { ...content, blocks: nextBlocks } };
  });
  return changed ? next : summaries;
}
function applyCommandImpl(doc, command, idGenerator) {
  switch (command.type) {
    case "undo":
    case "redo": {
      return { doc, result: { ok: true } };
    }
    case "set_node_content": {
      const { nodeId, content, plainText, assets } = command.payload;
      const node = doc.nodes[nodeId];
      if (!node) {
        return { doc, result: { ok: false, error: `Node not found: ${nodeId}` } };
      }
      const nextNode = {
        ...node,
        content: content ?? void 0,
        text: plainText
      };
      const nextAssets = assets ? { ...doc.assets ?? {}, ...assets } : doc.assets;
      return {
        doc: {
          ...doc,
          nodes: {
            ...doc.nodes,
            [nodeId]: nextNode
          },
          assets: nextAssets
        },
        result: { ok: true }
      };
    }
    case "set_summary_content": {
      const { summaryId, content, plainText, assets } = command.payload;
      const index = doc.summaries.findIndex((summary2) => summary2.id === summaryId);
      if (index === -1) {
        return { doc, result: { ok: false, error: `Summary not found: ${summaryId}` } };
      }
      const nextSummaries = [...doc.summaries];
      const summary = nextSummaries[index];
      nextSummaries[index] = { ...summary, content: content ?? void 0, text: plainText };
      const nextAssets = assets ? { ...doc.assets ?? {}, ...assets } : doc.assets;
      return {
        doc: {
          ...doc,
          summaries: nextSummaries,
          assets: nextAssets
        },
        result: { ok: true }
      };
    }
    case "set_node_attrs": {
      const { nodeId, attrs } = command.payload;
      const node = doc.nodes[nodeId];
      if (!node) {
        return { doc, result: { ok: false, error: `Node not found: ${nodeId}` } };
      }
      const nextNode = {
        ...node,
        attrs: attrs ?? void 0
      };
      return {
        doc: {
          ...doc,
          nodes: {
            ...doc.nodes,
            [nodeId]: nextNode
          }
        },
        result: { ok: true }
      };
    }
    case "set_node_data": {
      const { nodeId, data } = command.payload;
      const node = doc.nodes[nodeId];
      if (!node) {
        return { doc, result: { ok: false, error: `Node not found: ${nodeId}` } };
      }
      const nextNode = {
        ...node,
        data: data ?? void 0
      };
      return {
        doc: {
          ...doc,
          nodes: {
            ...doc.nodes,
            [nodeId]: nextNode
          }
        },
        result: { ok: true }
      };
    }
    case "set_node_submap": {
      const { nodeId, subMapId } = command.payload;
      const node = doc.nodes[nodeId];
      if (!node) {
        return { doc, result: { ok: false, error: `Node not found: ${nodeId}` } };
      }
      const nextNode = {
        ...node,
        subMapId: subMapId ?? void 0
      };
      return {
        doc: {
          ...doc,
          nodes: {
            ...doc.nodes,
            [nodeId]: nextNode
          }
        },
        result: { ok: true }
      };
    }
    case "set_node_content_width": {
      const { nodeId, contentWidth, width, mode } = command.payload;
      const node = doc.nodes[nodeId];
      if (!node) {
        return { doc, result: { ok: false, error: `Node not found: ${nodeId}` } };
      }
      const nextContentWidth = (() => {
        if (contentWidth !== void 0) {
          if (contentWidth === null) return null;
          const normalized = normalizeNodeContentWidth(contentWidth);
          if (!normalized) return null;
          if (normalized.mode === "fixed") {
            return resolveNodeFixedContentWidth(node, normalized.width, {
              restoreAutoWrapWidth: normalized.restoreAutoWrapWidth
            });
          }
          if (normalized.wrapWidth !== void 0) {
            return normalized;
          }
          return resolveNodeAutoContentWidth(node);
        }
        if (mode === null) return null;
        if (mode === "fixed") {
          const nextWidth = typeof width === "number" && Number.isFinite(width) ? Math.round(width) : resolveNodeContentWidth(node).width;
          return resolveNodeFixedContentWidth(node, nextWidth);
        }
        if (mode === "auto") {
          if (typeof width === "number" && Number.isFinite(width)) {
            return { mode: "auto", wrapWidth: Math.round(width) };
          }
          return resolveNodeAutoContentWidth(node);
        }
        if (typeof width === "number" && Number.isFinite(width)) {
          const current = resolveNodeContentWidth(node);
          if (current.mode === "fixed") {
            return resolveNodeFixedContentWidth(node, Math.round(width));
          }
          return { mode: "auto", wrapWidth: Math.round(width) };
        }
        if (width === null) return null;
        return normalizeNodeContentWidth(node.contentWidth) ?? null;
      })();
      const nextNode = applyNodeContentWidth(node, nextContentWidth);
      return {
        doc: {
          ...doc,
          nodes: {
            ...doc.nodes,
            [nodeId]: nextNode
          }
        },
        result: { ok: true }
      };
    }
    case "set_blur_view_state": {
      const { blur } = command.payload;
      const previousViewState = doc.viewState;
      const nextViewState = (() => {
        if (blur) {
          return { ...previousViewState ?? {}, blur };
        }
        if (!previousViewState) return void 0;
        const { blur: _removed, ...rest } = previousViewState;
        return Object.keys(rest).length > 0 ? rest : void 0;
      })();
      return {
        doc: {
          ...doc,
          viewState: nextViewState
        },
        result: { ok: true }
      };
    }
    case "toggle_node_collapsed": {
      const { nodeId } = command.payload;
      const node = doc.nodes[nodeId];
      if (!node) return { doc, result: { ok: false, error: `Node not found: ${nodeId}` } };
      const previous = doc.viewState?.collapsedNodeIds?.[nodeId] ?? false;
      const nextCollapsed = !previous;
      const nextMap = { ...doc.viewState?.collapsedNodeIds ?? {} };
      if (nextCollapsed) nextMap[nodeId] = true;
      else delete nextMap[nodeId];
      const nextViewState = (() => {
        const base = { ...doc.viewState ?? {} };
        if (Object.keys(nextMap).length > 0) base.collapsedNodeIds = nextMap;
        else delete base.collapsedNodeIds;
        return Object.keys(base).length > 0 ? base : void 0;
      })();
      return { doc: { ...doc, viewState: nextViewState }, result: { ok: true } };
    }
    case "set_node_collapsed": {
      const { nodeId, collapsed } = command.payload;
      const node = doc.nodes[nodeId];
      if (!node) return { doc, result: { ok: false, error: `Node not found: ${nodeId}` } };
      const nextMap = { ...doc.viewState?.collapsedNodeIds ?? {} };
      if (collapsed) nextMap[nodeId] = true;
      else delete nextMap[nodeId];
      const nextViewState = (() => {
        const base = { ...doc.viewState ?? {} };
        if (Object.keys(nextMap).length > 0) base.collapsedNodeIds = nextMap;
        else delete base.collapsedNodeIds;
        return Object.keys(base).length > 0 ? base : void 0;
      })();
      return { doc: { ...doc, viewState: nextViewState }, result: { ok: true } };
    }
    case "clear_mindmap_both_pins": {
      const { containerId } = command.payload;
      const container = doc.nodes[containerId];
      if (!container) return { doc, result: { ok: false, error: `Node not found: ${containerId}` } };
      if (!doc.roots.includes(containerId)) {
        return { doc, result: { ok: false, error: "clear_mindmap_both_pins: containerId must be a root (V1)" } };
      }
      const layoutType = container.layout ?? "logical-right";
      if (layoutType !== "mindmap-both" && layoutType !== "mindmap-both-auto") {
        return {
          doc,
          result: {
            ok: false,
            error: `clear_mindmap_both_pins: unsupported root layout ${layoutType}`
          }
        };
      }
      let changed = false;
      const nextNodes = { ...doc.nodes };
      for (const childId of container.children) {
        const child = nextNodes[childId];
        if (!child) continue;
        if (child.branchSide === void 0) continue;
        changed = true;
        const { branchSide: _removed, ...rest } = child;
        nextNodes[childId] = rest;
      }
      if (!changed) return { doc, result: { ok: true } };
      return { doc: { ...doc, nodes: nextNodes }, result: { ok: true } };
    }
    case "rebalance_mindmap_both_auto": {
      const { containerId } = command.payload;
      const container = doc.nodes[containerId];
      if (!container) return { doc, result: { ok: false, error: `Node not found: ${containerId}` } };
      if (!doc.roots.includes(containerId)) {
        return { doc, result: { ok: false, error: "rebalance_mindmap_both_auto: containerId must be a root (V1)" } };
      }
      const layoutType = container.layout ?? "logical-right";
      if (layoutType !== "mindmap-both-auto") {
        return {
          doc,
          result: {
            ok: false,
            error: `rebalance_mindmap_both_auto: unsupported root layout ${layoutType}`
          }
        };
      }
      const summaryById = new Map(doc.summaries.map((summary) => [summary.id, summary]));
      const summaryIdsByParent = /* @__PURE__ */ new Map();
      for (const summary of doc.summaries) {
        const key = String(summary.parentId);
        const bucket = summaryIdsByParent.get(key);
        if (bucket) bucket.push(summary.id);
        else summaryIdsByParent.set(key, [summary.id]);
      }
      const isNodeCollapsed = (nodeId) => doc.viewState?.collapsedNodeIds?.[nodeId] === true;
      const subtreeNodeCountMemo = /* @__PURE__ */ new Map();
      const countVisibleSubtreeNodes = (startNodeId) => {
        const cached = subtreeNodeCountMemo.get(startNodeId);
        if (cached !== void 0) return cached;
        const stack = [startNodeId];
        const visited = /* @__PURE__ */ new Set();
        let count = 0;
        while (stack.length > 0) {
          const current = stack.pop();
          if (!current) break;
          if (visited.has(current)) continue;
          visited.add(current);
          const node = doc.nodes[current];
          if (node) {
            count += 1;
            const collapsed = isNodeCollapsed(node.id);
            if (!collapsed) {
              for (const childId of node.children) {
                if (!doc.nodes[childId]) continue;
                stack.push(childId);
              }
              const summaryIds = summaryIdsByParent.get(node.id);
              if (summaryIds) {
                for (const summaryId of summaryIds) stack.push(summaryId);
              }
            }
          }
          const summary = summaryById.get(current);
          if (summary) {
            for (const childId of summary.children) {
              if (!doc.nodes[childId]) continue;
              stack.push(childId);
            }
            const summaryIds = summaryIdsByParent.get(summary.id);
            if (summaryIds) {
              for (const summaryId of summaryIds) stack.push(summaryId);
            }
          }
        }
        subtreeNodeCountMemo.set(startNodeId, count);
        return count;
      };
      const weightByChild = /* @__PURE__ */ new Map();
      const getWeight = (id) => {
        const existing = weightByChild.get(id);
        if (existing !== void 0) return existing;
        const weight = countVisibleSubtreeNodes(id);
        weightByChild.set(id, weight);
        return weight;
      };
      let leftTotal = 0;
      let rightTotal = 0;
      const mapping = {};
      let tieFlip = "right";
      for (const childId of container.children) {
        const node = doc.nodes[childId];
        if (!node) continue;
        const weight = getWeight(childId);
        const side = leftTotal < rightTotal ? "left" : rightTotal < leftTotal ? "right" : tieFlip = tieFlip === "left" ? "right" : "left";
        mapping[childId] = side;
        if (side === "left") leftTotal += weight;
        else rightTotal += weight;
      }
      let changed = false;
      const nextNodes = { ...doc.nodes };
      for (const childId of container.children) {
        const child = nextNodes[childId];
        const nextSide = mapping[childId];
        if (!child || !nextSide) continue;
        if (child.branchSide === nextSide) continue;
        changed = true;
        nextNodes[childId] = { ...child, branchSide: nextSide };
      }
      if (!changed) return { doc, result: { ok: true } };
      return { doc: { ...doc, nodes: nextNodes }, result: { ok: true } };
    }
    case "set_node_text": {
      const { nodeId, text } = command.payload;
      const node = doc.nodes[nodeId];
      if (!node) {
        return { doc, result: { ok: false, error: `Node not found: ${nodeId}` } };
      }
      const nextNode = {
        ...node,
        text
      };
      return {
        doc: {
          ...doc,
          nodes: {
            ...doc.nodes,
            [nodeId]: nextNode
          }
        },
        result: { ok: true }
      };
    }
    case "add_child": {
      const { parentId, index, node: partialNode } = command.payload;
      const parent = doc.nodes[parentId];
      if (!parent) {
        return { doc, result: { ok: false, error: `Node not found: ${parentId}` } };
      }
      const createdNodeId = idGenerator.generate("node");
      const insertIndex = typeof index === "number" ? clampIndex(index, parent.children.length) : parent.children.length;
      const leftSiblingId = insertIndex > 0 ? parent.children[insertIndex - 1] ?? null : null;
      const rightSiblingId = insertIndex < parent.children.length ? parent.children[insertIndex] ?? null : null;
      const leftPos = leftSiblingId ? doc.nodes[leftSiblingId]?.pos ?? null : null;
      const rightPos = rightSiblingId ? doc.nodes[rightSiblingId]?.pos ?? null : null;
      const nextPos = posBetween(leftPos, rightPos);
      const childNode = createNode(createdNodeId, {
        parentId,
        text: partialNode?.text ?? "",
        contentWidth: partialNode?.contentWidth,
        maxWidth: partialNode?.maxWidth,
        contentWidthMode: partialNode?.contentWidthMode,
        pos: nextPos
      });
      const nextChildren = [...parent.children];
      nextChildren.splice(insertIndex, 0, createdNodeId);
      const nextParent = {
        ...parent,
        children: nextChildren
      };
      return {
        doc: {
          ...doc,
          nodes: {
            ...doc.nodes,
            [createdNodeId]: childNode,
            [parentId]: nextParent
          }
        },
        result: { ok: true, createdNodeId }
      };
    }
    case "add_summary_child": {
      const { summaryId, index: childIndex, node: partialNode } = command.payload;
      const index = doc.summaries.findIndex((summary2) => summary2.id === summaryId);
      if (index === -1) {
        return { doc, result: { ok: false, error: `Summary not found: ${summaryId}` } };
      }
      const summary = doc.summaries[index];
      const createdNodeId = idGenerator.generate("node");
      const insertIndex = typeof childIndex === "number" ? clampIndex(childIndex, summary.children.length) : summary.children.length;
      const leftSiblingId = insertIndex > 0 ? summary.children[insertIndex - 1] ?? null : null;
      const rightSiblingId = insertIndex < summary.children.length ? summary.children[insertIndex] ?? null : null;
      const leftPos = leftSiblingId ? doc.nodes[leftSiblingId]?.pos ?? null : null;
      const rightPos = rightSiblingId ? doc.nodes[rightSiblingId]?.pos ?? null : null;
      const nextPos = posBetween(leftPos, rightPos);
      const childNode = createNode(createdNodeId, {
        parentSummaryId: summaryId,
        text: partialNode?.text ?? "",
        contentWidth: partialNode?.contentWidth,
        maxWidth: partialNode?.maxWidth,
        contentWidthMode: partialNode?.contentWidthMode,
        pos: nextPos
      });
      const nextSummaries = [...doc.summaries];
      const nextChildren = [...summary.children];
      nextChildren.splice(insertIndex, 0, createdNodeId);
      nextSummaries[index] = {
        ...summary,
        children: nextChildren
      };
      return {
        doc: {
          ...doc,
          nodes: {
            ...doc.nodes,
            [createdNodeId]: childNode
          },
          summaries: nextSummaries
        },
        result: { ok: true, createdNodeId }
      };
    }
    case "add_root": {
      const createdNodeId = idGenerator.generate("node");
      const partialNode = command.payload?.node;
      const requestedPosition = command.payload?.position;
      const insertIndex = typeof command.payload?.index === "number" ? clampIndex(command.payload.index, doc.roots.length) : doc.roots.length;
      const leftRootId = insertIndex > 0 ? doc.roots[insertIndex - 1] ?? null : null;
      const rightRootId = insertIndex < doc.roots.length ? doc.roots[insertIndex] ?? null : null;
      const leftPos = leftRootId ? doc.nodes[leftRootId]?.pos ?? null : null;
      const rightPos = rightRootId ? doc.nodes[rightRootId]?.pos ?? null : null;
      const nextPos = posBetween(leftPos, rightPos);
      const rootNode = createNode(createdNodeId, {
        text: partialNode?.text ?? "Root",
        contentWidth: partialNode?.contentWidth ?? { mode: "auto", wrapWidth: partialNode?.maxWidth ?? 240 },
        maxWidth: partialNode?.maxWidth ?? 240,
        contentWidthMode: partialNode?.contentWidthMode,
        layout: partialNode?.layout,
        pos: nextPos
      });
      const nextRoots = [...doc.roots];
      nextRoots.splice(insertIndex, 0, createdNodeId);
      const nextRootPositions = seedMissingRootPositions({ roots: nextRoots, existing: doc.rootPositions });
      if (requestedPosition && Number.isFinite(requestedPosition.x) && Number.isFinite(requestedPosition.y)) {
        nextRootPositions[createdNodeId] = { x: requestedPosition.x, y: requestedPosition.y };
      }
      return {
        doc: {
          ...doc,
          roots: nextRoots,
          rootPositions: nextRootPositions,
          nodes: {
            ...doc.nodes,
            [createdNodeId]: rootNode
          }
        },
        result: { ok: true, createdNodeId }
      };
    }
    case "move_root": {
      const { rootId, direction } = command.payload;
      const index = doc.roots.indexOf(rootId);
      if (index === -1) {
        return { doc, result: { ok: false, error: `Root not found: ${rootId}` } };
      }
      const nextIndex = direction === "up" ? index - 1 : index + 1;
      if (nextIndex < 0 || nextIndex >= doc.roots.length) {
        return { doc, result: { ok: true } };
      }
      const nextRoots = [...doc.roots];
      nextRoots.splice(index, 1);
      nextRoots.splice(nextIndex, 0, rootId);
      const leftId = nextIndex > 0 ? nextRoots[nextIndex - 1] : null;
      const rightId = nextIndex < nextRoots.length - 1 ? nextRoots[nextIndex + 1] : null;
      const leftPos = leftId ? doc.nodes[leftId]?.pos ?? null : null;
      const rightPos = rightId ? doc.nodes[rightId]?.pos ?? null : null;
      const node = doc.nodes[rootId];
      const nextPos = posBetween(leftPos, rightPos);
      return {
        doc: {
          ...doc,
          roots: nextRoots,
          nodes: node ? { ...doc.nodes, [rootId]: { ...node, pos: nextPos } } : doc.nodes
        },
        result: { ok: true }
      };
    }
    case "set_node_layout": {
      const { nodeId, layout } = command.payload;
      const node = doc.nodes[nodeId];
      if (!node) {
        return { doc, result: { ok: false, error: `Node not found: ${nodeId}` } };
      }
      return {
        doc: {
          ...doc,
          nodes: {
            ...doc.nodes,
            [nodeId]: {
              ...node,
              layout: layout ?? void 0
            }
          }
        },
        result: { ok: true }
      };
    }
    case "delete_node": {
      const { nodeId } = command.payload;
      const node = doc.nodes[nodeId];
      if (!node) {
        return { doc, result: { ok: false, error: `Node not found: ${nodeId}` } };
      }
      const isRoot = doc.roots.includes(nodeId);
      if (isRoot && doc.roots.length <= 1) {
        return { doc, result: { ok: false, error: "Cannot delete the last root" } };
      }
      const summariesByParent = buildSummariesByParent(doc);
      const deletedNodeIds = new Set(collectSubtreeIds(doc, nodeId, summariesByParent));
      const nextNodes = { ...doc.nodes };
      for (const id of deletedNodeIds) {
        delete nextNodes[id];
      }
      const nextRoots = doc.roots.filter((id) => !deletedNodeIds.has(id));
      const sanitized = sanitizeSummaries({
        nodes: nextNodes,
        roots: nextRoots,
        summaries: doc.summaries,
        originalSummaries: doc.summaries
      });
      const rootPositions = doc.rootPositions ?? {};
      const sanitizedRootSet = new Set(sanitized.roots);
      const sanitizedRootPositions = {};
      for (const [id, position] of Object.entries(rootPositions)) {
        if (!sanitizedRootSet.has(id)) continue;
        sanitizedRootPositions[id] = position;
      }
      const collapsedNodeIds = doc.viewState?.collapsedNodeIds;
      const sanitizedCollapsedNodeIds = collapsedNodeIds ? Object.fromEntries(
        Object.entries(collapsedNodeIds).filter(([id, value]) => !deletedNodeIds.has(id) && value === true)
      ) : void 0;
      const nextViewState = (() => {
        if (!doc.viewState) return void 0;
        const next = { ...doc.viewState };
        if (sanitizedCollapsedNodeIds && Object.keys(sanitizedCollapsedNodeIds).length > 0) next.collapsedNodeIds = sanitizedCollapsedNodeIds;
        else delete next.collapsedNodeIds;
        return Object.keys(next).length > 0 ? next : void 0;
      })();
      const nodes = pruneDanglingInternalLinks(sanitized.nodes, deletedNodeIds);
      const summaries = pruneDanglingInternalLinksInSummaries(sanitized.summaries, deletedNodeIds);
      return {
        doc: {
          ...doc,
          roots: sanitized.roots,
          nodes,
          summaries,
          rootPositions: sanitizedRootPositions,
          relations: doc.relations.filter((rel) => {
            const nextDoc = { ...doc, roots: nextRoots, nodes, summaries };
            return relationEndpointExists(nextDoc, rel.from) && relationEndpointExists(nextDoc, rel.to);
          }),
          viewState: nextViewState
        },
        result: { ok: true }
      };
    }
    case "create_summary": {
      const { parentId, childIds, summary: partial } = command.payload;
      const parentNode = doc.nodes[parentId];
      const parentSummary = doc.summaries.find((item) => item.id === parentId);
      if (!parentNode && !parentSummary) {
        return { doc, result: { ok: false, error: `Parent not found: ${parentId}` } };
      }
      const uniqueChildIds = Array.from(new Set(childIds)).filter((id) => Boolean(doc.nodes[id]));
      if (uniqueChildIds.length === 0) {
        return { doc, result: { ok: false, error: "Summary must include at least one child node" } };
      }
      for (const childId of uniqueChildIds) {
        const child = doc.nodes[childId];
        const isValid = parentNode ? child?.parentId === parentId : child?.parentSummaryId === parentId;
        if (!isValid) {
          return {
            doc,
            result: { ok: false, error: `Summary child must be a direct child of ${parentId}: ${childId}` }
          };
        }
      }
      const containerChildIds = (() => {
        if (parentSummary) return parentSummary.children.filter((id) => Boolean(doc.nodes[id]));
        if (!parentNode) return [];
        const layoutType = parentNode.layout ?? "logical-right";
        if (layoutType !== "mindmap-both" && layoutType !== "mindmap-both-auto") {
          return parentNode.children.filter((id) => Boolean(doc.nodes[id]));
        }
        const resolveSide = (nodeId) => doc.nodes[nodeId]?.branchSide === "left" ? "left" : "right";
        const selectedSides = new Set(uniqueChildIds.map((id) => resolveSide(id)));
        if (selectedSides.size > 1) {
          return [];
        }
        const targetSide = selectedSides.has("left") ? "left" : "right";
        return parentNode.children.filter((id) => Boolean(doc.nodes[id]) && resolveSide(id) === targetSide);
      })();
      if (containerChildIds.length === 0) {
        if (parentNode && (parentNode.layout === "mindmap-both" || parentNode.layout === "mindmap-both-auto")) {
          return { doc, result: { ok: false, error: `${parentNode.layout}: summary selection must stay on the same side (left/right)` } };
        }
      }
      const indexById = new Map(containerChildIds.map((id, index) => [id, index]));
      const indices = uniqueChildIds.map((id) => indexById.get(id)).filter((index) => index !== void 0);
      if (indices.length !== uniqueChildIds.length) {
        return { doc, result: { ok: false, error: "Summary childIds must belong to the same parent container" } };
      }
      const startIndex = Math.min(...indices);
      const endIndex = Math.max(...indices);
      const coveredIds = containerChildIds.slice(startIndex, endIndex + 1);
      const coveredSet = new Set(coveredIds);
      for (const id of uniqueChildIds) {
        if (!coveredSet.has(id)) {
          return { doc, result: { ok: false, error: "Summary selection must be contiguous siblings" } };
        }
      }
      for (const existing of doc.summaries) {
        if (existing.parentId !== parentId) continue;
        const existingIndices = existing.childIds.map((id) => indexById.get(id)).filter((index) => index !== void 0);
        if (existingIndices.length !== existing.childIds.length) continue;
        if (existingIndices.length === 0) continue;
        const existingStart = Math.min(...existingIndices);
        const existingEnd = Math.max(...existingIndices);
        if (endIndex < existingStart || startIndex > existingEnd) continue;
        if (startIndex === existingStart && endIndex === existingEnd) {
          return { doc, result: { ok: true, createdSummaryId: existing.id } };
        }
        return { doc, result: { ok: false, error: `Summary overlaps with existing summary: ${existing.id}` } };
      }
      const createdSummaryId = idGenerator.generate("summary");
      const summary = {
        id: createdSummaryId,
        parentId,
        childIds: coveredIds,
        text: partial?.text ?? "",
        content: partial?.content,
        maxWidth: partial?.maxWidth,
        layout: partial?.layout,
        children: []
      };
      return {
        doc: {
          ...doc,
          summaries: [...doc.summaries, summary]
        },
        result: { ok: true, createdSummaryId }
      };
    }
    case "update_summary_text": {
      const { summaryId, text } = command.payload;
      const index = doc.summaries.findIndex((summary) => summary.id === summaryId);
      if (index === -1) {
        return { doc, result: { ok: false, error: `Summary not found: ${summaryId}` } };
      }
      const nextSummaries = [...doc.summaries];
      nextSummaries[index] = { ...nextSummaries[index], text };
      return { doc: { ...doc, summaries: nextSummaries }, result: { ok: true } };
    }
    case "set_summary_layout": {
      const { summaryId, layout } = command.payload;
      const index = doc.summaries.findIndex((summary) => summary.id === summaryId);
      if (index === -1) {
        return { doc, result: { ok: false, error: `Summary not found: ${summaryId}` } };
      }
      const nextSummaries = [...doc.summaries];
      nextSummaries[index] = {
        ...nextSummaries[index],
        layout: layout ?? void 0
      };
      return { doc: { ...doc, summaries: nextSummaries }, result: { ok: true } };
    }
    case "delete_summary": {
      const { summaryId } = command.payload;
      const index = doc.summaries.findIndex((summary) => summary.id === summaryId);
      if (index === -1) {
        return { doc, result: { ok: false, error: `Summary not found: ${summaryId}` } };
      }
      const summariesByParent = buildSummariesByParent(doc);
      const deletedNodeIds = new Set(
        collectSubtreeIds(doc, summaryId, summariesByParent)
      );
      const nextNodes = { ...doc.nodes };
      for (const id of deletedNodeIds) {
        delete nextNodes[id];
      }
      const nextRoots = doc.roots.filter((id) => !deletedNodeIds.has(id));
      const nextSummaries = doc.summaries.filter((item) => item.id !== summaryId);
      const sanitized = sanitizeSummaries({
        nodes: nextNodes,
        roots: nextRoots,
        summaries: nextSummaries,
        originalSummaries: doc.summaries
      });
      const nodes = pruneDanglingInternalLinks(sanitized.nodes, deletedNodeIds);
      const summaries = pruneDanglingInternalLinksInSummaries(sanitized.summaries, deletedNodeIds);
      return {
        doc: {
          ...doc,
          roots: sanitized.roots,
          nodes,
          summaries,
          relations: doc.relations.filter((rel) => {
            const nextDoc = { ...doc, roots: nextRoots, nodes, summaries };
            return relationEndpointExists(nextDoc, rel.from) && relationEndpointExists(nextDoc, rel.to);
          })
        },
        result: { ok: true }
      };
    }
    case "create_relation": {
      const { label, style } = command.payload;
      const from = normalizeRelationEndpoint(command.payload.from);
      const to = normalizeRelationEndpoint(command.payload.to);
      if (!from) {
        return { doc, result: { ok: false, error: "Invalid relation source endpoint" } };
      }
      if (!to) {
        return { doc, result: { ok: false, error: "Invalid relation target endpoint" } };
      }
      if (!relationEndpointExists(doc, from)) {
        return { doc, result: { ok: false, error: `Relation endpoint not found: ${relationEndpointKey(from)}` } };
      }
      if (!relationEndpointExists(doc, to)) {
        return { doc, result: { ok: false, error: `Relation endpoint not found: ${relationEndpointKey(to)}` } };
      }
      if (relationEndpointKey(from) === relationEndpointKey(to)) {
        return { doc, result: { ok: false, error: "Cannot create a relation to itself" } };
      }
      const createdRelationId = idGenerator.generate("relation");
      const relation = {
        id: createdRelationId,
        from,
        to,
        routeType: "curved",
        direction: normalizeRelationDirection(command.payload.direction) ?? "forward",
        label,
        style
      };
      return {
        doc: { ...doc, relations: [...doc.relations, relation] },
        result: { ok: true, createdRelationId }
      };
    }
    case "delete_relation": {
      const { relationId } = command.payload;
      const nextRelations = doc.relations.filter((rel) => rel.id !== relationId);
      if (nextRelations.length === doc.relations.length) {
        return { doc, result: { ok: false, error: `Relation not found: ${relationId}` } };
      }
      return { doc: { ...doc, relations: nextRelations }, result: { ok: true } };
    }
    case "set_relation_label": {
      const { relationId, label } = command.payload;
      const index = doc.relations.findIndex((rel) => rel.id === relationId);
      if (index === -1) {
        return { doc, result: { ok: false, error: `Relation not found: ${relationId}` } };
      }
      const normalized = (() => {
        if (!label) return void 0;
        if (label.schemaVersion !== 1) return void 0;
        if (label.kind !== "plain-text") return void 0;
        const text = String(label.text ?? "");
        if (text.trim().length === 0) return void 0;
        return { ...label, text };
      })();
      const prev = doc.relations[index];
      const next = { ...prev, label: normalized };
      const nextRelations = doc.relations.slice();
      nextRelations[index] = next;
      return { doc: { ...doc, relations: nextRelations }, result: { ok: true } };
    }
    case "set_relation_direction": {
      const { relationId, direction } = command.payload;
      const index = doc.relations.findIndex((rel) => rel.id === relationId);
      if (index === -1) {
        return { doc, result: { ok: false, error: `Relation not found: ${relationId}` } };
      }
      const normalizedDirection = direction == null ? void 0 : normalizeRelationDirection(direction);
      const prev = doc.relations[index];
      const next = { ...prev, direction: normalizedDirection };
      const nextRelations = doc.relations.slice();
      nextRelations[index] = next;
      const currentTheme = ensureDocumentTheme(doc);
      const overrides = { ...currentTheme.overrides ?? {} };
      const relations = { ...overrides.relations ?? {} };
      const relationOverride = { ...relations[relationId] ?? {} };
      if (normalizedDirection) {
        relationOverride.direction = normalizedDirection;
        relations[relationId] = relationOverride;
      } else {
        delete relationOverride.direction;
        if (Object.keys(relationOverride).length > 0) relations[relationId] = relationOverride;
        else delete relations[relationId];
      }
      const nextOverrides = {
        ...overrides,
        relations: Object.keys(relations).length > 0 ? relations : void 0
      };
      const nextTheme = {
        ...currentTheme,
        overrides: Object.values(nextOverrides).some((value) => value !== void 0) ? nextOverrides : void 0
      };
      return { doc: { ...doc, relations: nextRelations, theme: nextTheme }, result: { ok: true } };
    }
    case "set_relation_style": {
      const { relationId, style } = command.payload;
      const index = doc.relations.findIndex((rel) => rel.id === relationId);
      if (index === -1) {
        return { doc, result: { ok: false, error: `Relation not found: ${relationId}` } };
      }
      const normalized = (() => {
        if (!style) return void 0;
        const next2 = {
          strokeColor: style.strokeColor,
          strokeWidth: style.strokeWidth,
          strokeDasharray: style.strokeDasharray
        };
        const hasAny = Boolean(next2.strokeColor || next2.strokeDasharray || typeof next2.strokeWidth === "number" && !Number.isNaN(next2.strokeWidth));
        if (!hasAny) return void 0;
        return next2;
      })();
      const prev = doc.relations[index];
      const next = { ...prev, style: normalized };
      const nextRelations = doc.relations.slice();
      nextRelations[index] = next;
      return { doc: { ...doc, relations: nextRelations }, result: { ok: true } };
    }
    case "set_relation_curve": {
      const { relationId, curve } = command.payload;
      const index = doc.relations.findIndex((rel) => rel.id === relationId);
      if (index === -1) {
        return { doc, result: { ok: false, error: `Relation not found: ${relationId}` } };
      }
      const normalized = (() => {
        if (!curve) return void 0;
        if (curve.schemaVersion !== 1) return void 0;
        if (curve.kind !== "cubic") return void 0;
        return {
          ...curve,
          control1: { x: Number(curve.control1.x ?? 0), y: Number(curve.control1.y ?? 0) },
          control2: { x: Number(curve.control2.x ?? 0), y: Number(curve.control2.y ?? 0) }
        };
      })();
      const prev = doc.relations[index];
      const next = { ...prev, curve: normalized };
      const nextRelations = doc.relations.slice();
      nextRelations[index] = next;
      return { doc: { ...doc, relations: nextRelations }, result: { ok: true } };
    }
    case "set_relation_ports": {
      const { relationId, fromPort, toPort } = command.payload;
      const index = doc.relations.findIndex((rel) => rel.id === relationId);
      if (index === -1) {
        return { doc, result: { ok: false, error: `Relation not found: ${relationId}` } };
      }
      const prev = doc.relations[index];
      const nextFromPort = fromPort == null ? void 0 : fromPort;
      const nextToPort = toPort == null ? void 0 : toPort;
      const nextFromPortRatio = (() => {
        if (!nextFromPort) return void 0;
        return prev.from.port === nextFromPort ? prev.from.portRatio : void 0;
      })();
      const nextToPortRatio = (() => {
        if (!nextToPort) return void 0;
        return prev.to.port === nextToPort ? prev.to.portRatio : void 0;
      })();
      const next = {
        ...prev,
        from: { ...prev.from, port: nextFromPort, portRatio: nextFromPortRatio },
        to: { ...prev.to, port: nextToPort, portRatio: nextToPortRatio }
      };
      const nextRelations = doc.relations.slice();
      nextRelations[index] = next;
      return { doc: { ...doc, relations: nextRelations }, result: { ok: true } };
    }
    case "set_relation_endpoint": {
      const { relationId, endpoint, port, portRatio } = command.payload;
      const index = doc.relations.findIndex((rel) => rel.id === relationId);
      if (index === -1) {
        return { doc, result: { ok: false, error: `Relation not found: ${relationId}` } };
      }
      const normalizeRatio = (value) => {
        if (value == null) return void 0;
        const next2 = Number(value);
        if (!Number.isFinite(next2)) return void 0;
        return Math.max(0, Math.min(1, next2));
      };
      const prev = doc.relations[index];
      const nextPort = port == null ? void 0 : port;
      const nextPortRatio = nextPort ? normalizeRatio(portRatio) : void 0;
      const next = {
        ...prev,
        [endpoint]: {
          ...endpoint === "from" ? prev.from : prev.to,
          port: nextPort,
          portRatio: nextPortRatio
        }
      };
      const nextRelations = doc.relations.slice();
      nextRelations[index] = next;
      return { doc: { ...doc, relations: nextRelations }, result: { ok: true } };
    }
    case "insert_subtree": {
      const { parentId, subtree } = command.payload;
      if (parentId && !doc.nodes[parentId]) {
        return { doc, result: { ok: false, error: `Node not found: ${parentId}` } };
      }
      const idMap = /* @__PURE__ */ new Map();
      for (const oldId of Object.keys(subtree.nodes)) {
        idMap.set(oldId, idGenerator.generate("node"));
      }
      const assetIdMap = /* @__PURE__ */ new Map();
      const subtreeAssets = subtree.assets ?? {};
      const nextNodes = { ...doc.nodes };
      for (const [oldId, oldNode] of Object.entries(subtree.nodes)) {
        const newId = idMap.get(oldId);
        if (!newId) continue;
        nextNodes[newId] = {
          ...oldNode,
          id: newId,
          // Best practice: when pasting subtree as a child, drop layout overrides to avoid
          // bringing in layouts that are invalid under the target root/subtree layout whitelist.
          // When pasting as new roots (parentId=null), keep the original root layout overrides.
          layout: parentId ? void 0 : oldNode.layout,
          parentId: oldNode.parentId ? idMap.get(oldNode.parentId) ?? void 0 : void 0,
          parentSummaryId: void 0,
          children: oldNode.children.map((childId) => idMap.get(childId) ?? childId),
          content: rewriteContentIds(oldNode.content, { nodeIdMap: idMap, assetIdMap })
        };
      }
      const newRootIds = subtree.roots.map((rootId) => idMap.get(rootId) ?? rootId);
      const nextAssets = { ...doc.assets ?? {} };
      for (const [assetId, asset] of Object.entries(subtreeAssets)) {
        if (nextAssets[assetId]) continue;
        nextAssets[assetId] = { ...asset, id: assetId };
      }
      let nextRoots = doc.roots;
      if (!parentId) {
        const lastRootId = doc.roots[doc.roots.length - 1] ?? null;
        let cursorPos = lastRootId ? doc.nodes[lastRootId]?.pos ?? null : null;
        for (const rootId of newRootIds) {
          const pastedRoot = nextNodes[rootId];
          if (!pastedRoot) continue;
          const nextPos = cursorPos ? posBetween(cursorPos, null) : posBetween(null, null);
          pastedRoot.pos = nextPos;
          cursorPos = nextPos;
        }
        nextRoots = [...doc.roots, ...newRootIds];
      } else {
        const parentNode = nextNodes[parentId] ?? doc.nodes[parentId];
        if (!parentNode) {
          return { doc, result: { ok: false, error: `Node not found: ${parentId}` } };
        }
        nextNodes[parentId] = {
          ...parentNode,
          children: [...parentNode.children, ...newRootIds]
        };
        const lastSiblingId = parentNode.children[parentNode.children.length - 1] ?? null;
        let cursorPos = lastSiblingId ? doc.nodes[lastSiblingId]?.pos ?? null : null;
        for (const rootId of newRootIds) {
          const pastedRoot = nextNodes[rootId];
          if (pastedRoot) {
            pastedRoot.parentId = parentId;
            const nextPos = cursorPos ? posBetween(cursorPos, null) : posBetween(null, null);
            pastedRoot.pos = nextPos;
            cursorPos = nextPos;
          }
        }
      }
      const nextRootPositions = !parentId ? seedMissingRootPositions({ roots: nextRoots, existing: doc.rootPositions }) : doc.rootPositions;
      return {
        doc: {
          ...doc,
          roots: nextRoots,
          rootPositions: nextRootPositions,
          nodes: nextNodes,
          assets: nextAssets
        },
        result: { ok: true }
      };
    }
    case "move_node": {
      const { nodeId, to } = command.payload;
      const node = doc.nodes[nodeId];
      if (!node) {
        return { doc, result: { ok: false, error: `Node not found: ${nodeId}` } };
      }
      const rootPositions = doc.rootPositions ?? {};
      const isRoot = doc.roots.includes(nodeId);
      const currentRootIndex = isRoot ? doc.roots.indexOf(nodeId) : -1;
      if (isRoot && doc.roots.length <= 1 && to.type !== "root") {
        return { doc, result: { ok: false, error: "Cannot move the last root" } };
      }
      if (to.type === "node" && !isRoot && !node.parentSummaryId && to.parentId === node.parentId) {
        const wantsBranchSideChange = (() => {
          if (to.branchSide === void 0) return false;
          const next = to.branchSide === null ? void 0 : to.branchSide;
          return node.branchSide !== next;
        })();
        if (to.index === void 0 && !wantsBranchSideChange) return { doc, result: { ok: true } };
        if (to.index === void 0) {
        } else {
          const parent = doc.nodes[to.parentId];
          if (parent) {
            const siblings = parent.children.filter((id) => id !== nodeId);
            const nextIndex = clampIndex(to.index, siblings.length);
            const nextChildren = [...siblings];
            nextChildren.splice(nextIndex, 0, nodeId);
            if (arraysEqual(nextChildren, parent.children) && !wantsBranchSideChange) {
              return { doc, result: { ok: true } };
            }
          }
        }
      }
      if (to.type === "summary" && !isRoot && !node.parentId && to.summaryId === node.parentSummaryId) {
        if (to.index === void 0) return { doc, result: { ok: true } };
        const summary = doc.summaries.find((item) => item.id === to.summaryId);
        if (summary) {
          const siblings = summary.children.filter((id) => id !== nodeId);
          const nextIndex = clampIndex(to.index, siblings.length);
          const nextChildren = [...siblings];
          nextChildren.splice(nextIndex, 0, nodeId);
          if (arraysEqual(nextChildren, summary.children)) {
            return { doc, result: { ok: true } };
          }
        }
      }
      if (to.type === "root" && isRoot && !node.parentId && !node.parentSummaryId) {
        const currentPosition = rootPositions[nodeId];
        const nextPosition = to.position;
        const positionUnchanged = !nextPosition ? currentPosition === void 0 : currentPosition !== void 0 && currentPosition.x === nextPosition.x && currentPosition.y === nextPosition.y;
        if (to.index === void 0) {
          if (positionUnchanged) return { doc, result: { ok: true } };
        } else {
          const rootsWithout = doc.roots.filter((id) => id !== nodeId);
          const nextIndex = clampIndex(to.index, rootsWithout.length);
          const nextRoots2 = [...rootsWithout];
          nextRoots2.splice(nextIndex, 0, nodeId);
          if (positionUnchanged && arraysEqual(nextRoots2, doc.roots)) {
            return { doc, result: { ok: true } };
          }
        }
      }
      const summariesByParent = buildSummariesByParent(doc);
      const descendants = new Set(collectSubtreeIds(doc, nodeId, summariesByParent));
      if (to.type === "node") {
        const parent = doc.nodes[to.parentId];
        if (!parent) {
          return { doc, result: { ok: false, error: `Node not found: ${to.parentId}` } };
        }
        if (descendants.has(to.parentId)) {
          return { doc, result: { ok: false, error: "Cannot move a node into its own subtree" } };
        }
      }
      if (to.type === "summary") {
        const summaryById = new Map(doc.summaries.map((item) => [item.id, item]));
        const summary = summaryById.get(to.summaryId);
        if (!summary) {
          return { doc, result: { ok: false, error: `Summary not found: ${to.summaryId}` } };
        }
        let anchorNodeId = null;
        let cursor = summary;
        const visitedSummaries = /* @__PURE__ */ new Set();
        while (cursor) {
          if (visitedSummaries.has(cursor.id)) break;
          visitedSummaries.add(cursor.id);
          const parentId = cursor.parentId;
          if (doc.nodes[parentId]) {
            anchorNodeId = parentId;
            break;
          }
          cursor = summaryById.get(parentId);
        }
        if (anchorNodeId && descendants.has(anchorNodeId)) {
          return { doc, result: { ok: false, error: "Cannot move a node into its own subtree" } };
        }
      }
      const nextNodes = { ...doc.nodes };
      let nextRoots = [...doc.roots];
      let nextSummaries = doc.summaries.map((summary) => ({ ...summary, childIds: [...summary.childIds], children: [...summary.children] }));
      const nextRootPositions = { ...rootPositions };
      if (isRoot) {
        nextRoots = nextRoots.filter((id) => id !== nodeId);
      } else if (node.parentId) {
        const parent = nextNodes[node.parentId];
        if (parent) {
          nextNodes[node.parentId] = { ...parent, children: parent.children.filter((id) => id !== nodeId) };
        }
      } else if (node.parentSummaryId) {
        nextSummaries = nextSummaries.map(
          (summary) => summary.id === node.parentSummaryId ? { ...summary, children: summary.children.filter((id) => id !== nodeId) } : summary
        );
      } else {
        for (const candidate of Object.values(nextNodes)) {
          if (!candidate.children.includes(nodeId)) continue;
          nextNodes[candidate.id] = { ...candidate, children: candidate.children.filter((id) => id !== nodeId) };
        }
        nextSummaries = nextSummaries.map((summary) => ({
          ...summary,
          children: summary.children.filter((id) => id !== nodeId)
        }));
      }
      if (isRoot && to.type !== "root") {
        delete nextRootPositions[nodeId];
      }
      const nextNode = { ...node, parentId: void 0, parentSummaryId: void 0 };
      if (to.type === "root") {
        const base = nextRoots.filter((id) => id !== nodeId);
        const insertIndex = typeof to.index === "number" ? clampIndex(to.index, base.length) : isRoot && currentRootIndex >= 0 ? clampIndex(currentRootIndex, base.length) : base.length;
        base.splice(insertIndex, 0, nodeId);
        nextRoots = base;
        const shouldUpdatePos = !isRoot || typeof to.index === "number";
        if (shouldUpdatePos) {
          const leftId = insertIndex > 0 ? base[insertIndex - 1] : null;
          const rightId = insertIndex < base.length - 1 ? base[insertIndex + 1] : null;
          const leftPos = leftId ? nextNodes[leftId]?.pos ?? doc.nodes[leftId]?.pos ?? null : null;
          const rightPos = rightId ? nextNodes[rightId]?.pos ?? doc.nodes[rightId]?.pos ?? null : null;
          nextNode.pos = posBetween(leftPos, rightPos);
        }
        if (to.position) {
          nextRootPositions[nodeId] = { x: to.position.x, y: to.position.y };
        } else if (!isRoot) {
          delete nextRootPositions[nodeId];
        }
      } else if (to.type === "node") {
        const parent = nextNodes[to.parentId];
        if (!parent) {
          return { doc, result: { ok: false, error: `Node not found: ${to.parentId}` } };
        }
        const wasSameParent = !isRoot && !node.parentSummaryId && node.parentId === to.parentId;
        nextNode.parentId = to.parentId;
        if (to.branchSide !== void 0) {
          nextNode.branchSide = to.branchSide === null ? void 0 : to.branchSide;
        }
        const siblings = parent.children.filter((id) => id !== nodeId);
        const insertIndex = (() => {
          if (typeof to.index === "number") return clampIndex(to.index, siblings.length);
          if (!wasSameParent) return siblings.length;
          const originalParent = doc.nodes[to.parentId];
          const originalIndex = originalParent ? originalParent.children.indexOf(nodeId) : -1;
          if (originalIndex < 0) return siblings.length;
          return clampIndex(originalIndex, siblings.length);
        })();
        siblings.splice(insertIndex, 0, nodeId);
        nextNodes[to.parentId] = { ...parent, children: siblings };
        const shouldUpdatePos = !wasSameParent || typeof to.index === "number";
        if (shouldUpdatePos) {
          const leftId = insertIndex > 0 ? siblings[insertIndex - 1] : null;
          const rightId = insertIndex < siblings.length - 1 ? siblings[insertIndex + 1] : null;
          const leftPos = leftId ? nextNodes[leftId]?.pos ?? doc.nodes[leftId]?.pos ?? null : null;
          const rightPos = rightId ? nextNodes[rightId]?.pos ?? doc.nodes[rightId]?.pos ?? null : null;
          nextNode.pos = posBetween(leftPos, rightPos);
        }
      } else {
        const wasSameSummary = !isRoot && !node.parentId && node.parentSummaryId === to.summaryId;
        nextNode.parentSummaryId = to.summaryId;
        const summaryIndex = nextSummaries.findIndex((summary2) => summary2.id === to.summaryId);
        if (summaryIndex === -1) {
          return { doc, result: { ok: false, error: `Summary not found: ${to.summaryId}` } };
        }
        const summary = nextSummaries[summaryIndex];
        const siblings = summary.children.filter((id) => id !== nodeId);
        const insertIndex = typeof to.index === "number" ? clampIndex(to.index, siblings.length) : siblings.length;
        siblings.splice(insertIndex, 0, nodeId);
        nextSummaries = nextSummaries.slice();
        nextSummaries[summaryIndex] = { ...summary, children: siblings };
        const shouldUpdatePos = !wasSameSummary || typeof to.index === "number";
        if (shouldUpdatePos) {
          const leftId = insertIndex > 0 ? siblings[insertIndex - 1] : null;
          const rightId = insertIndex < siblings.length - 1 ? siblings[insertIndex + 1] : null;
          const leftPos = leftId ? nextNodes[leftId]?.pos ?? doc.nodes[leftId]?.pos ?? null : null;
          const rightPos = rightId ? nextNodes[rightId]?.pos ?? doc.nodes[rightId]?.pos ?? null : null;
          nextNode.pos = posBetween(leftPos, rightPos);
        }
      }
      nextNodes[nodeId] = nextNode;
      const sanitized = sanitizeSummaries({
        nodes: nextNodes,
        roots: nextRoots,
        summaries: nextSummaries,
        originalSummaries: doc.summaries
      });
      const sanitizedRootSet = new Set(sanitized.roots);
      const sanitizedRootPositions = {};
      for (const [id, position] of Object.entries(nextRootPositions)) {
        if (!sanitizedRootSet.has(id)) continue;
        sanitizedRootPositions[id] = position;
      }
      return {
        doc: {
          ...doc,
          roots: sanitized.roots,
          nodes: sanitized.nodes,
          summaries: sanitized.summaries,
          rootPositions: sanitizedRootPositions
        },
        result: { ok: true }
      };
    }
    case "set_document_theme": {
      const currentTheme = ensureDocumentTheme(doc);
      const nextTheme = {
        ...currentTheme,
        defaultTheme: command.payload.theme
      };
      return {
        doc: { ...doc, theme: nextTheme },
        result: { ok: true }
      };
    }
    case "set_root_theme": {
      const { rootId, theme } = command.payload;
      if (!doc.roots.includes(rootId)) {
        return { doc, result: { ok: false, error: `Root not found: ${rootId}` } };
      }
      const currentTheme = ensureDocumentTheme(doc);
      const rootThemes = { ...currentTheme.rootThemes ?? {} };
      if (theme) {
        rootThemes[rootId] = theme;
      } else {
        delete rootThemes[rootId];
      }
      const nextTheme = {
        ...currentTheme,
        rootThemes: Object.keys(rootThemes).length > 0 ? rootThemes : void 0
      };
      return {
        doc: { ...doc, theme: nextTheme },
        result: { ok: true }
      };
    }
    case "set_theme_root_edge_route": {
      const { rootId, routeType } = command.payload;
      if (!doc.roots.includes(rootId)) {
        return { doc, result: { ok: false, error: `Root not found: ${rootId}` } };
      }
      const currentTheme = ensureDocumentTheme(doc);
      const rootEdgeRoutes = { ...currentTheme.rootEdgeRoutes ?? {} };
      if (routeType) {
        rootEdgeRoutes[rootId] = routeType;
      } else {
        delete rootEdgeRoutes[rootId];
      }
      const nextTheme = {
        ...currentTheme,
        rootEdgeRoutes: Object.keys(rootEdgeRoutes).length > 0 ? rootEdgeRoutes : void 0
      };
      return {
        doc: { ...doc, theme: nextTheme },
        result: { ok: true }
      };
    }
    case "set_theme_root_rainbow_enabled": {
      const { rootId, enabled } = command.payload;
      if (!doc.roots.includes(rootId)) {
        return { doc, result: { ok: false, error: `Root not found: ${rootId}` } };
      }
      const currentTheme = ensureDocumentTheme(doc);
      const rootRainbowEdges = { ...currentTheme.rootRainbowEdges ?? {} };
      if (enabled === null) {
        delete rootRainbowEdges[rootId];
      } else {
        rootRainbowEdges[rootId] = Boolean(enabled);
      }
      const nextTheme = {
        ...currentTheme,
        rootRainbowEdges: Object.keys(rootRainbowEdges).length > 0 ? rootRainbowEdges : void 0
      };
      return {
        doc: { ...doc, theme: nextTheme },
        result: { ok: true }
      };
    }
    case "set_theme_edge_style_scope": {
      const { nodeId, patch } = command.payload;
      if (!doc.nodes[nodeId]) {
        return { doc, result: { ok: false, error: `Node not found: ${nodeId}` } };
      }
      const currentTheme = ensureDocumentTheme(doc);
      const edgeStyleScopes = { ...currentTheme.edgeStyleScopes ?? {} };
      if (patch) {
        edgeStyleScopes[nodeId] = patch;
      } else {
        delete edgeStyleScopes[nodeId];
      }
      const nextTheme = {
        ...currentTheme,
        edgeStyleScopes: Object.keys(edgeStyleScopes).length > 0 ? edgeStyleScopes : void 0
      };
      return {
        doc: { ...doc, theme: nextTheme },
        result: { ok: true }
      };
    }
    case "set_theme_relation_style": {
      const currentTheme = ensureDocumentTheme(doc);
      const patch = normalizeThemeRelationOverride(command.payload.patch);
      const nextTheme = {
        ...currentTheme,
        relationStyle: patch
      };
      return { doc: { ...doc, theme: nextTheme }, result: { ok: true } };
    }
    case "set_theme_root_relation_style": {
      const { rootId } = command.payload;
      if (!doc.roots.includes(rootId)) {
        return { doc, result: { ok: false, error: `Root not found: ${rootId}` } };
      }
      const currentTheme = ensureDocumentTheme(doc);
      const rootRelationStyles = { ...currentTheme.rootRelationStyles ?? {} };
      const patch = normalizeThemeRelationOverride(command.payload.patch);
      if (patch) {
        rootRelationStyles[rootId] = patch;
      } else {
        delete rootRelationStyles[rootId];
      }
      const nextTheme = {
        ...currentTheme,
        rootRelationStyles: Object.keys(rootRelationStyles).length > 0 ? rootRelationStyles : void 0
      };
      return { doc: { ...doc, theme: nextTheme }, result: { ok: true } };
    }
    case "set_theme_appearance": {
      const currentTheme = ensureDocumentTheme(doc);
      const nextTheme = {
        ...currentTheme,
        appearance: command.payload.appearance ?? void 0
      };
      return { doc: { ...doc, theme: nextTheme }, result: { ok: true } };
    }
    case "set_theme_rainbow": {
      const currentTheme = ensureDocumentTheme(doc);
      const currentRainbow = currentTheme.rainbow ?? { enabled: false, branchColors: {}, paletteOverride: void 0 };
      const paletteOverrideRaw = command.payload.paletteOverride;
      const wantsClearPaletteOverride = paletteOverrideRaw === null;
      const explicitPalette = Array.isArray(paletteOverrideRaw) ? paletteOverrideRaw : void 0;
      const storedPaletteOverride = !wantsClearPaletteOverride && Array.isArray(currentRainbow.paletteOverride) ? currentRainbow.paletteOverride : void 0;
      const nextPaletteOverride = explicitPalette ?? storedPaletteOverride;
      let nextTheme = {
        ...currentTheme,
        rainbow: {
          ...currentRainbow,
          enabled: Boolean(command.payload.enabled),
          paletteOverride: nextPaletteOverride,
          branchColors: currentRainbow.branchColors ?? {}
        }
      };
      if (nextTheme.rainbow?.enabled) {
        const variantId = resolveThemeVariantId(currentTheme.appearance, {});
        for (const rootId of doc.roots) {
          const root = doc.nodes[rootId];
          if (!root) continue;
          const themeRef = currentTheme.rootThemes?.[rootId] ?? currentTheme.defaultTheme;
          const themeDefinition = resolveThemeDefinition(themeRef, doc.assets ?? {}) ?? createDefaultThemeDefinition();
          const variant = resolveThemeVariant(themeDefinition, variantId);
          const themePalette = Array.isArray(variant.rainbow?.palette) ? variant.rainbow.palette : void 0;
          const palette = explicitPalette ?? storedPaletteOverride ?? themePalette ?? DEFAULT_RAINBOW_PALETTE;
          for (const childId of root.children) {
            if (!doc.nodes[childId]) continue;
            nextTheme = ensureRainbowBranchColor(nextTheme, childId, palette);
          }
        }
      }
      return { doc: { ...doc, theme: nextTheme }, result: { ok: true } };
    }
    case "set_theme_rainbow_branch_color": {
      const { branchId, color } = command.payload;
      const currentTheme = ensureDocumentTheme(doc);
      const rainbow = currentTheme.rainbow ?? { enabled: false, branchColors: {}, paletteOverride: void 0 };
      const branchColors = { ...rainbow.branchColors ?? {} };
      if (color) {
        branchColors[branchId] = color;
      } else {
        delete branchColors[branchId];
      }
      const nextTheme = {
        ...currentTheme,
        rainbow: {
          ...rainbow,
          branchColors
        }
      };
      return { doc: { ...doc, theme: nextTheme }, result: { ok: true } };
    }
    case "set_theme_node_override": {
      const { nodeId, patch } = command.payload;
      if (!doc.nodes[nodeId]) {
        return { doc, result: { ok: false, error: `Node not found: ${nodeId}` } };
      }
      const currentTheme = ensureDocumentTheme(doc);
      const overrides = { ...currentTheme.overrides ?? {} };
      const nodes = { ...overrides.nodes ?? {} };
      if (patch) {
        nodes[nodeId] = patch;
      } else {
        delete nodes[nodeId];
      }
      overrides.nodes = Object.keys(nodes).length > 0 ? nodes : void 0;
      const nextTheme = {
        ...currentTheme,
        overrides: Object.keys(overrides).length > 0 ? overrides : void 0
      };
      return { doc: { ...doc, theme: nextTheme }, result: { ok: true } };
    }
    case "upsert_assets": {
      const nextAssets = { ...doc.assets ?? {}, ...command.payload.assets };
      return {
        doc: { ...doc, assets: nextAssets },
        result: { ok: true }
      };
    }
    case "materialize_theme_asset": {
      const currentTheme = ensureDocumentTheme(doc);
      const assetId = generateUniqueAssetId(doc.assets ?? {}, idGenerator);
      const asset = { id: assetId, kind: "json", data: command.payload.theme };
      const nextAssets = { ...doc.assets ?? {}, [assetId]: asset };
      const themeRef = { source: "asset", assetId };
      let nextTheme = currentTheme;
      if (command.payload.scope === "document") {
        nextTheme = { ...currentTheme, defaultTheme: themeRef };
      } else {
        if (!doc.roots.includes(command.payload.rootId)) {
          return { doc, result: { ok: false, error: `Root not found: ${command.payload.rootId}` } };
        }
        const rootThemes = { ...currentTheme.rootThemes ?? {} };
        rootThemes[command.payload.rootId] = themeRef;
        nextTheme = { ...currentTheme, rootThemes };
      }
      return {
        doc: { ...doc, assets: nextAssets, theme: nextTheme },
        result: { ok: true, createdAssetId: assetId }
      };
    }
  }
}
function ensureDocumentTheme(doc) {
  const assets = doc.assets ?? {};
  const normalized = normalizeThemeState(doc.theme, assets);
  if (normalized) return normalized;
  return createDefaultDocumentThemeState({
    source: "inline",
    value: createDefaultThemeDefinition()
  });
}
function generateUniqueAssetId(existing, idGenerator) {
  for (let attempt = 0; attempt < 50; attempt += 1) {
    const candidate = idGenerator.generate("asset");
    if (!existing[candidate]) return candidate;
  }
  let counter = 0;
  while (true) {
    const candidate = `${idGenerator.generate("asset")}_${counter}`;
    if (!existing[candidate]) return candidate;
    counter += 1;
  }
}
function rewriteContentIds(content, maps) {
  if (!content) return content;
  if (content.schemaVersion !== 1) return content;
  if (content.kind === "blocks") {
    const nextBlocks = content.blocks.map((block) => {
      if (block.type === "image") {
        const remapped = maps.assetIdMap.get(block.assetId);
        return remapped ? { ...block, assetId: remapped } : block;
      }
      if (block.type === "embed") {
        const assetId = block.embed.assetId;
        if (!assetId) return block;
        const remapped = maps.assetIdMap.get(assetId);
        return remapped ? { ...block, embed: { ...block.embed, assetId: remapped } } : block;
      }
      if (block.type === "links") {
        const nextLinks = block.links.map((link) => {
          if (link.kind !== "internal") return link;
          if (typeof link.docId === "string" && link.docId.trim().length > 0) return link;
          const remapped = maps.nodeIdMap.get(link.nodeId);
          return remapped ? { ...link, nodeId: remapped } : link;
        });
        return { ...block, links: nextLinks };
      }
      return block;
    });
    return { ...content, blocks: nextBlocks };
  }
  return content;
}
function clampIndex(index, length) {
  if (!Number.isFinite(index)) return length;
  return Math.max(0, Math.min(length, Math.trunc(index)));
}
function arraysEqual(a, b) {
  if (a.length !== b.length) return false;
  for (let index = 0; index < a.length; index += 1) {
    if (a[index] !== b[index]) return false;
  }
  return true;
}
function shouldCanonicalizeTree(command) {
  switch (command.type) {
    case "add_child":
    case "add_summary_child":
    case "add_root":
    case "move_root":
    case "delete_node":
    case "insert_subtree":
    case "move_node":
    case "delete_summary":
      return true;
    default:
      return false;
  }
}
function canonicalizeTree(doc) {
  const normalized = normalizeTree(doc);
  const rootPositions = seedMissingRootPositions({ roots: normalized.roots, existing: normalized.rootPositions });
  return { ...normalized, rootPositions };
}
function applyCommand(doc, command, idGenerator) {
  const out = applyCommandImpl(doc, command, idGenerator);
  if (!out.result.ok) return out;
  if (out.doc === doc) return out;
  if (!shouldCanonicalizeTree(command)) return out;
  return { ...out, doc: canonicalizeTree(out.doc) };
}
var init_commands = __esm({
  "../core/src/commands.ts"() {
    "use strict";
    init_document();
    init_node_content_width();
    init_theme();
    init_root_positions();
    init_summaries();
    init_pos();
    init_tree();
    init_relations();
  }
});

// ../core/src/id.ts
function createKmindId(prefix, options) {
  const normalizedPrefix = sanitizeKmindIdPrefix(prefix);
  const now = typeof options?.now === "number" && Number.isFinite(options.now) ? options.now : Date.now();
  return `${normalizedPrefix}_${formatUtcTimestamp(now)}_${createUlid(now)}`;
}
function formatUtcTimestamp(now) {
  const date = new Date(now);
  const yyyy = String(date.getUTCFullYear()).padStart(4, "0");
  const MM = String(date.getUTCMonth() + 1).padStart(2, "0");
  const dd = String(date.getUTCDate()).padStart(2, "0");
  const hh = String(date.getUTCHours()).padStart(2, "0");
  const mm = String(date.getUTCMinutes()).padStart(2, "0");
  const ss = String(date.getUTCSeconds()).padStart(2, "0");
  const SSS = String(date.getUTCMilliseconds()).padStart(3, "0");
  return `${yyyy}${MM}${dd}T${hh}${mm}${ss}${SSS}Z`;
}
function createUlid(now) {
  const time = Math.max(0, Math.min(Number.isFinite(now) ? Math.trunc(now) : 0, 281474976710655));
  return `${encodeBase32(time, 10)}${encodeRandomBase32(16)}`;
}
function sanitizeKmindIdPrefix(prefix) {
  const trimmed = String(prefix ?? "").trim();
  const safe = trimmed.replace(/[^a-zA-Z0-9_-]/g, "_").replace(/_+/g, "_").replace(/^_+/, "").replace(/_+$/, "");
  return safe || "id";
}
function encodeBase32(value, length) {
  let remaining = value;
  let out = "";
  for (let i = 0; i < length; i += 1) {
    const mod = remaining % 32;
    out = `${CROCKFORD_BASE32[mod] ?? "0"}${out}`;
    remaining = Math.floor(remaining / 32);
  }
  return out;
}
function encodeRandomBase32(length) {
  const bytes = new Uint8Array(length);
  fillRandomBytes(bytes);
  let out = "";
  for (const byte of bytes) {
    out += CROCKFORD_BASE32[byte & 31] ?? "0";
  }
  return out;
}
function fillRandomBytes(bytes) {
  const cryptoObj = globalThis.crypto;
  if (cryptoObj && typeof cryptoObj.getRandomValues === "function") {
    cryptoObj.getRandomValues(bytes);
    return;
  }
  for (let i = 0; i < bytes.length; i += 1) {
    bytes[i] = Math.floor(Math.random() * 256);
  }
}
var CROCKFORD_BASE32, DefaultIdGenerator;
var init_id = __esm({
  "../core/src/id.ts"() {
    "use strict";
    CROCKFORD_BASE32 = "0123456789ABCDEFGHJKMNPQRSTVWXYZ";
    DefaultIdGenerator = class {
      generate(kind) {
        switch (kind) {
          case "node":
            return createKmindId("n");
          case "summary":
            return createKmindId("summary");
          case "relation":
            return createKmindId("rel");
          case "asset":
            return createKmindId("asset");
        }
      }
    };
  }
});

// ../core/src/core.ts
function normalizeDocument(doc, idGenerator) {
  const rawSummaries = Array.isArray(doc.summaries) ? doc.summaries : [];
  const rawRelations = Array.isArray(doc.relations) ? doc.relations : [];
  const rawRootPositions = doc.rootPositions;
  const rawAssets = doc.assets;
  const rawViewState = doc.viewState;
  const rawTheme = doc.theme;
  const rawRoots = Array.isArray(doc.roots) ? doc.roots : [];
  const normalizedSummaries = rawSummaries.map((summary) => {
    const children = Array.isArray(summary.children) ? summary.children : [];
    return {
      ...summary,
      children: children.filter((id) => typeof id === "string")
    };
  });
  const normalized = {
    ...doc,
    summaries: normalizedSummaries,
    relations: rawRelations,
    rootPositions: normalizeRootPositions(rawRootPositions, rawRoots),
    assets: normalizeAssets(rawAssets),
    viewState: normalizeViewState(rawViewState),
    theme: void 0
  };
  const assets = normalized.assets ?? {};
  const normalizedTheme = normalizeThemeState(rawTheme, assets) ?? createDefaultDocumentThemeState({
    source: "inline",
    value: createDefaultThemeDefinition()
  });
  normalized.theme = normalizedTheme;
  const treeNormalized = normalizeTree(normalized);
  const roots = treeNormalized.roots;
  treeNormalized.rootPositions = seedMissingRootPositions({
    roots,
    existing: normalizeRootPositions(treeNormalized.rootPositions, roots)
  });
  treeNormalized.relations = rawRelations.map((relation) => normalizeRelationForDocument(treeNormalized, relation)).filter((relation) => Boolean(relation));
  if (treeNormalized.roots.length > 0) return treeNormalized;
  return createDocument(idGenerator);
}
function normalizeRootPositions(raw, roots) {
  if (!raw || typeof raw !== "object" || Array.isArray(raw)) return {};
  const result2 = {};
  const rootSet = new Set(roots);
  for (const [key, value] of Object.entries(raw)) {
    if (!rootSet.has(key)) continue;
    if (!value || typeof value !== "object" || Array.isArray(value)) continue;
    const x = value.x;
    const y = value.y;
    if (typeof x !== "number" || !Number.isFinite(x)) continue;
    if (typeof y !== "number" || !Number.isFinite(y)) continue;
    result2[key] = { x, y };
  }
  return result2;
}
function normalizeAssets(raw) {
  if (!raw || typeof raw !== "object" || Array.isArray(raw)) return {};
  const next = {};
  for (const [id, value] of Object.entries(raw)) {
    if (!value || typeof value !== "object" || Array.isArray(value)) continue;
    const kind = value.kind;
    if (kind === "image" || kind === "blob") {
      const mimeType = value.mimeType;
      const dataUrl = value.dataUrl;
      if (typeof mimeType !== "string" || typeof dataUrl !== "string") continue;
      const width = value.width;
      const height = value.height;
      next[id] = {
        ...value,
        id,
        kind,
        mimeType,
        dataUrl,
        width: typeof width === "number" ? width : void 0,
        height: typeof height === "number" ? height : void 0
      };
      continue;
    }
    if (kind === "json") {
      next[id] = {
        ...value,
        id,
        kind: "json"
      };
    }
  }
  return next;
}
function normalizeViewState(raw) {
  if (!raw || typeof raw !== "object" || Array.isArray(raw)) return void 0;
  const result2 = {};
  const blur = raw.blur;
  if (blur && typeof blur === "object" && !Array.isArray(blur)) {
    const defaultVisibility = blur.defaultVisibility;
    if (defaultVisibility === "hidden" || defaultVisibility === "revealed") {
      const nodeOverrides = blur.nodeOverrides;
      const segmentOverrides = blur.segmentOverrides;
      result2.blur = {
        defaultVisibility,
        nodeOverrides: nodeOverrides && typeof nodeOverrides === "object" && !Array.isArray(nodeOverrides) ? nodeOverrides : void 0,
        segmentOverrides: segmentOverrides && typeof segmentOverrides === "object" && !Array.isArray(segmentOverrides) ? segmentOverrides : void 0
      };
    }
  }
  const collapsedNodeIdsRaw = raw.collapsedNodeIds;
  if (collapsedNodeIdsRaw && typeof collapsedNodeIdsRaw === "object" && !Array.isArray(collapsedNodeIdsRaw)) {
    const collapsedNodeIds = {};
    for (const [id, value] of Object.entries(collapsedNodeIdsRaw)) {
      if (typeof value !== "boolean") continue;
      collapsedNodeIds[id] = value;
    }
    if (Object.keys(collapsedNodeIds).length > 0) {
      result2.collapsedNodeIds = collapsedNodeIds;
    }
  }
  return Object.keys(result2).length > 0 ? result2 : void 0;
}
function cloneDocument(doc) {
  if (typeof structuredClone === "function") {
    return structuredClone(doc);
  }
  return JSON.parse(JSON.stringify(doc));
}
var MindMapCore;
var init_core = __esm({
  "../core/src/core.ts"() {
    "use strict";
    init_commands();
    init_id();
    init_document();
    init_theme();
    init_root_positions();
    init_tree();
    init_relations();
    MindMapCore = class {
      id;
      listeners = /* @__PURE__ */ new Set();
      idGenerator;
      state;
      history;
      maxHistory;
      constructor(options = {}) {
        this.id = options.id ?? "kmind";
        this.idGenerator = options.idGenerator ?? new DefaultIdGenerator();
        this.maxHistory = options.maxHistory ?? 200;
        this.history = { past: [], future: [] };
        const initialDocument = options.initialDocument ?? createDocument(this.idGenerator);
        this.state = { document: normalizeDocument(cloneDocument(initialDocument), this.idGenerator) };
      }
      getState() {
        return this.state;
      }
      subscribe(listener) {
        this.listeners.add(listener);
        return () => {
          this.listeners.delete(listener);
        };
      }
      dispatch(command) {
        if (command.type === "undo") {
          return this.undo();
        }
        if (command.type === "redo") {
          return this.redo();
        }
        const currentDoc = this.state.document;
        const { doc: nextDoc, result: result2 } = applyCommand(currentDoc, command, this.idGenerator);
        if (!result2.ok) return result2;
        if (nextDoc === currentDoc) return result2;
        this.pushHistory(currentDoc);
        this.state = {
          ...this.state,
          document: nextDoc
        };
        this.emit();
        return result2;
      }
      dispatchBatch(commands) {
        if (!Array.isArray(commands) || commands.length === 0) return { ok: true, results: [] };
        for (const command of commands) {
          if (command.type === "undo" || command.type === "redo") {
            return { ok: false, error: "dispatchBatch does not support undo/redo commands" };
          }
        }
        const currentDoc = this.state.document;
        let workingDoc = currentDoc;
        const results = [];
        for (const command of commands) {
          const { doc: nextDoc, result: result2 } = applyCommand(workingDoc, command, this.idGenerator);
          if (!result2.ok) {
            return { ok: false, error: result2.error };
          }
          results.push(result2);
          workingDoc = nextDoc;
        }
        if (workingDoc !== currentDoc) {
          this.pushHistory(currentDoc);
          this.state = { ...this.state, document: workingDoc };
          this.emit();
        }
        return { ok: true, results };
      }
      toJSON() {
        return cloneDocument(this.state.document);
      }
      fromJSON(doc) {
        const nextDoc = normalizeDocument(cloneDocument(doc), this.idGenerator);
        this.history = { past: [], future: [] };
        this.state = { ...this.state, document: nextDoc };
        this.emit();
      }
      getNode(nodeId) {
        return this.state.document.nodes[nodeId];
      }
      canUndo() {
        return this.history.past.length > 0;
      }
      canRedo() {
        return this.history.future.length > 0;
      }
      undo() {
        const previous = this.history.past.pop();
        if (!previous) return { ok: false, error: "Nothing to undo" };
        const current = this.state.document;
        this.history.future.push(current);
        this.state = { ...this.state, document: previous };
        this.emit();
        return { ok: true };
      }
      redo() {
        const next = this.history.future.pop();
        if (!next) return { ok: false, error: "Nothing to redo" };
        const current = this.state.document;
        this.history.past.push(current);
        this.state = { ...this.state, document: next };
        this.emit();
        return { ok: true };
      }
      emit() {
        for (const listener of this.listeners) {
          listener();
        }
      }
      pushHistory(doc) {
        this.history.past.push(doc);
        if (this.history.past.length > this.maxHistory) {
          this.history.past.splice(0, this.history.past.length - this.maxHistory);
        }
        this.history.future = [];
      }
    };
  }
});

// ../core/src/blur.ts
var init_blur = __esm({
  "../core/src/blur.ts"() {
    "use strict";
  }
});

// ../core/src/content.ts
var init_content = __esm({
  "../core/src/content.ts"() {
    "use strict";
  }
});

// ../core/src/compact-document.ts
var init_compact_document = __esm({
  "../core/src/compact-document.ts"() {
    "use strict";
    init_theme();
    init_summaries();
    init_relations();
  }
});

// ../core/src/layout/logical-right.ts
var init_logical_right = __esm({
  "../core/src/layout/logical-right.ts"() {
    "use strict";
  }
});

// ../core/src/layout/tree-down.ts
var init_tree_down = __esm({
  "../core/src/layout/tree-down.ts"() {
    "use strict";
  }
});

// ../core/src/layout/mindmap-legacy.ts
var init_mindmap_legacy = __esm({
  "../core/src/layout/mindmap-legacy.ts"() {
    "use strict";
    init_relations();
  }
});

// ../core/src/layout/mindmap-tidy.ts
var init_mindmap_tidy = __esm({
  "../core/src/layout/mindmap-tidy.ts"() {
    "use strict";
    init_relations();
  }
});

// ../core/src/layout/mindmap.ts
var init_mindmap = __esm({
  "../core/src/layout/mindmap.ts"() {
    "use strict";
    init_mindmap_legacy();
    init_mindmap_tidy();
  }
});

// ../core/src/layout/index.ts
var init_layout = __esm({
  "../core/src/layout/index.ts"() {
    "use strict";
    init_logical_right();
    init_tree_down();
    init_mindmap();
  }
});

// ../core/src/edge-router.ts
var init_edge_router = __esm({
  "../core/src/edge-router.ts"() {
    "use strict";
  }
});

// ../core/src/drag/drop-intent.ts
var init_drop_intent = __esm({
  "../core/src/drag/drop-intent.ts"() {
    "use strict";
  }
});

// ../core/src/drag/drop-intent-v2.ts
var init_drop_intent_v2 = __esm({
  "../core/src/drag/drop-intent-v2.ts"() {
    "use strict";
    init_drop_intent();
  }
});

// ../core/src/drag/index.ts
var init_drag = __esm({
  "../core/src/drag/index.ts"() {
    "use strict";
    init_drop_intent();
    init_drop_intent_v2();
  }
});

// ../core/src/index.ts
var init_src = __esm({
  "../core/src/index.ts"() {
    "use strict";
    init_commands();
    init_core();
    init_blur();
    init_theme();
    init_content();
    init_document();
    init_node_content_width();
    init_compact_document();
    init_relations();
    init_pos();
    init_tree();
    init_id();
    init_id();
    init_layout();
    init_edge_router();
    init_drag();
    init_drag();
  }
});

// ../collab/dist/kmind-crdt-v1.js
var init_kmind_crdt_v1 = __esm({
  "../collab/dist/kmind-crdt-v1.js"() {
    "use strict";
    init_src();
  }
});

// ../collab/dist/crdt-mindmap-core.js
var init_crdt_mindmap_core = __esm({
  "../collab/dist/crdt-mindmap-core.js"() {
    "use strict";
    init_src();
    init_kmind_crdt_v1();
  }
});

// ../collab/dist/index.js
var init_dist = __esm({
  "../collab/dist/index.js"() {
    "use strict";
    init_broadcast_channel_sync();
    init_yjs_helpers();
    init_crdt_mindmap_core();
    init_kmind_crdt_v1();
  }
});

// src/commands/export.ts
import { parseArgs } from "node:util";

// ../app/src/features/document-feature.ts
init_dist();
init_src();

// ../themes/src/presets.ts
init_src();

// ../themes/src/themes/baseline-fork-ink.ts
var baselineForkInkTheme = {
  schemaVersion: 1,
  id: "kmind-baseline-fork-ink",
  name: "Baseline Fork Ink",
  description: "Heavy ink baseline branches inspired by classic skeleton mind maps.",
  variants: {
    light: {
      tokens: {
        layout: {
          fontFamily: "ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif",
          fontSize: 15,
          fontWeight: 700,
          lineHeight: 1.24,
          textAlign: "left",
          paddingX: 9,
          paddingY: 8,
          nodeMinWidth: 76,
          nodeMinHeight: 34
        },
        paint: {
          bg: "#ffffff",
          panel: "#ffffff",
          text: "#111111",
          muted: "#525252",
          border: "#d4d4d4",
          nodeFill: "transparent",
          nodeFillSelected: "rgba(37, 99, 235, 0.08)",
          nodeStroke: "transparent",
          nodeStrokeSelected: "#3749b5",
          edgeStroke: "#151515",
          relationStroke: "#737373",
          relationStrokeSelected: "#3749b5",
          summaryStroke: "#151515"
        }
      },
      background: { color: "#ffffff" },
      edges: {
        routeType: "baseline-fork",
        strokeWidth: 4,
        cap: "butt",
        join: "miter",
        routeOptions: {
          "baseline-fork": {
            lead: 16,
            baselineOffset: 7,
            diagonalAngle: 64
          }
        }
      },
      relations: {
        strokeWidth: 2,
        cap: "round",
        join: "round"
      },
      nodeShape: {
        type: "rect",
        strokeWidth: 0
      },
      rainbow: {
        enabled: false,
        palette: ["#151515", "#3749b5", "#525252", "#737373"]
      },
      rules: {
        nodeRules: [
          {
            id: "baseline-root",
            priority: 10,
            when: { kind: "depth", depth: 0 },
            apply: {
              layout: {
                fontFamily: "ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, 'Liberation Mono', monospace",
                fontSize: 26,
                fontWeight: 800,
                textAlign: "center",
                paddingX: 12,
                paddingY: 8
              },
              paint: {
                text: "#3749b5",
                nodeFill: "transparent",
                nodeStroke: "transparent"
              },
              nodeShape: {
                type: "rect",
                strokeWidth: 0
              }
            }
          },
          {
            id: "baseline-depth-1",
            priority: 10,
            when: { kind: "depth", depth: 1 },
            apply: {
              layout: { fontSize: 18, fontWeight: 760, paddingX: 10, paddingY: 8 },
              incomingEdge: { strokeColor: "#151515", strokeWidth: 4, routeType: "baseline-fork" }
            }
          },
          {
            id: "baseline-depth-2",
            priority: 10,
            when: { kind: "depth", depth: 2 },
            apply: {
              layout: { fontSize: 15, fontWeight: 700, paddingX: 9, paddingY: 7 },
              incomingEdge: { strokeColor: "#151515", strokeWidth: 4, routeType: "baseline-fork" }
            }
          },
          {
            id: "baseline-depth-3plus",
            priority: 10,
            when: { kind: "depthRange", minDepth: 3 },
            apply: {
              layout: { fontSize: 14, fontWeight: 680, paddingX: 8, paddingY: 7 },
              incomingEdge: { strokeColor: "#151515", strokeWidth: 3.5, routeType: "baseline-fork" }
            }
          }
        ]
      }
    },
    dark: {
      tokens: {
        layout: {
          fontFamily: "ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif",
          fontSize: 15,
          fontWeight: 700,
          lineHeight: 1.24,
          textAlign: "left",
          paddingX: 9,
          paddingY: 8,
          nodeMinWidth: 76,
          nodeMinHeight: 34
        },
        paint: {
          bg: "#0a0a0a",
          panel: "#111111",
          text: "#f5f5f5",
          muted: "#a3a3a3",
          border: "#404040",
          nodeFill: "transparent",
          nodeFillSelected: "rgba(147, 197, 253, 0.12)",
          nodeStroke: "transparent",
          nodeStrokeSelected: "#93a4ff",
          edgeStroke: "#f5f5f5",
          relationStroke: "#a3a3a3",
          relationStrokeSelected: "#93a4ff",
          summaryStroke: "#f5f5f5"
        }
      },
      background: { color: "#0a0a0a" },
      edges: {
        routeType: "baseline-fork",
        strokeWidth: 4,
        cap: "butt",
        join: "miter",
        routeOptions: {
          "baseline-fork": {
            lead: 16,
            baselineOffset: 7,
            diagonalAngle: 64
          }
        }
      },
      relations: {
        strokeWidth: 2,
        cap: "round",
        join: "round"
      },
      nodeShape: {
        type: "rect",
        strokeWidth: 0
      },
      rainbow: {
        enabled: false,
        palette: ["#f5f5f5", "#93a4ff", "#d4d4d4", "#a3a3a3"]
      },
      rules: {
        nodeRules: [
          {
            id: "baseline-root",
            priority: 10,
            when: { kind: "depth", depth: 0 },
            apply: {
              layout: {
                fontFamily: "ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, 'Liberation Mono', monospace",
                fontSize: 26,
                fontWeight: 800,
                textAlign: "center",
                paddingX: 12,
                paddingY: 8
              },
              paint: {
                text: "#93a4ff",
                nodeFill: "transparent",
                nodeStroke: "transparent"
              },
              nodeShape: {
                type: "rect",
                strokeWidth: 0
              }
            }
          },
          {
            id: "baseline-depth-1",
            priority: 10,
            when: { kind: "depth", depth: 1 },
            apply: {
              layout: { fontSize: 18, fontWeight: 760, paddingX: 10, paddingY: 8 },
              incomingEdge: { strokeColor: "#f5f5f5", strokeWidth: 4, routeType: "baseline-fork" }
            }
          },
          {
            id: "baseline-depth-2",
            priority: 10,
            when: { kind: "depth", depth: 2 },
            apply: {
              layout: { fontSize: 15, fontWeight: 700, paddingX: 9, paddingY: 7 },
              incomingEdge: { strokeColor: "#f5f5f5", strokeWidth: 4, routeType: "baseline-fork" }
            }
          },
          {
            id: "baseline-depth-3plus",
            priority: 10,
            when: { kind: "depthRange", minDepth: 3 },
            apply: {
              layout: { fontSize: 14, fontWeight: 680, paddingX: 8, paddingY: 7 },
              incomingEdge: { strokeColor: "#f5f5f5", strokeWidth: 3.5, routeType: "baseline-fork" }
            }
          }
        ]
      }
    }
  }
};

// ../themes/src/themes/candy-pop.ts
init_src();
function deepClone(value) {
  const clone = globalThis.structuredClone;
  if (typeof clone === "function") return clone(value);
  return JSON.parse(JSON.stringify(value));
}
var candyPopTheme = (() => {
  const theme = deepClone(createDefaultThemeDefinition());
  theme.id = "kmind-candy-pop";
  theme.name = "Candy Pop";
  theme.variants.light.tokens.paint = {
    ...theme.variants.light.tokens.paint,
    bg: "#fff1f2",
    panel: "#ffffff",
    text: "#111827",
    muted: "#6b7280",
    border: "#fecdd3",
    nodeFill: "#ffffff",
    nodeFillSelected: "rgba(236, 72, 153, 0.12)",
    nodeStroke: "#ec4899",
    nodeStrokeSelected: "#7c3aed",
    edgeStroke: "#7c3aed",
    summaryStroke: "rgba(124, 58, 237, 0.55)",
    relationStroke: "#0ea5e9",
    relationStrokeSelected: "#f97316"
  };
  theme.variants.light.nodeShape = { type: "pill", strokeWidth: 2.5 };
  theme.variants.dark.tokens.paint = {
    ...theme.variants.dark.tokens.paint,
    bg: "#0b1020",
    panel: "#0f172a",
    text: "#e5e7eb",
    muted: "#94a3b8",
    border: "rgba(148, 163, 184, 0.18)",
    nodeFill: "#0f172a",
    nodeFillSelected: "rgba(236, 72, 153, 0.18)",
    nodeStroke: "#fb7185",
    nodeStrokeSelected: "#a78bfa",
    edgeStroke: "#a78bfa",
    summaryStroke: "rgba(167, 139, 250, 0.55)",
    relationStroke: "#38bdf8",
    relationStrokeSelected: "#fb7185"
  };
  theme.variants.dark.nodeShape = { type: "pill", strokeWidth: 2.5 };
  return theme;
})();

// ../themes/src/themes/material-3.ts
init_src();
function deepClone2(value) {
  const clone = globalThis.structuredClone;
  if (typeof clone === "function") return clone(value);
  return JSON.parse(JSON.stringify(value));
}
var material3Theme = (() => {
  const theme = deepClone2(createDefaultThemeDefinition());
  theme.id = "kmind-material-3";
  theme.name = "Material 3";
  theme.variants.light.tokens.layout = {
    ...theme.variants.light.tokens.layout,
    fontFamily: "ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif",
    fontSize: 14,
    fontWeight: 450,
    lineHeight: 1.45,
    paddingX: 14,
    paddingY: 10,
    nodeMinHeight: 40
  };
  theme.variants.light.tokens.paint = {
    ...theme.variants.light.tokens.paint,
    bg: "#fef7ff",
    panel: "#ffffff",
    text: "#1c1b1f",
    muted: "#49454f",
    border: "#e7e0ec",
    nodeFill: "#f3edf7",
    nodeFillSelected: "#eaddff",
    nodeStroke: "transparent",
    nodeStrokeSelected: "#6750a4",
    edgeStroke: "#79747e",
    summaryStroke: "#cac4d0",
    relationStroke: "#7d5260",
    relationStrokeSelected: "#b3261e"
  };
  theme.variants.light.background = { color: "#fef7ff" };
  theme.variants.light.edges = { strokeWidth: 2, dasharray: "6 4", cap: "round", join: "round" };
  theme.variants.light.nodeShape = { type: "rounded-rect", radius: 16, strokeWidth: 0 };
  theme.variants.dark.tokens.layout = deepClone2(theme.variants.light.tokens.layout);
  theme.variants.dark.tokens.paint = {
    ...theme.variants.dark.tokens.paint,
    bg: "#141218",
    panel: "#1d1b20",
    text: "#e6e1e5",
    muted: "#cac4d0",
    border: "rgba(202, 196, 208, 0.22)",
    nodeFill: "#211f26",
    nodeFillSelected: "#4f378b",
    nodeStroke: "transparent",
    nodeStrokeSelected: "#d0bcff",
    edgeStroke: "#938f99",
    summaryStroke: "#49454f",
    relationStroke: "#efb8c8",
    relationStrokeSelected: "#f2b8b5"
  };
  theme.variants.dark.background = { color: "#141218" };
  theme.variants.dark.edges = deepClone2(theme.variants.light.edges);
  theme.variants.dark.nodeShape = deepClone2(theme.variants.light.nodeShape);
  const rulesLight = [
    {
      id: "m3-root",
      priority: 10,
      when: { kind: "depth", depth: 0 },
      apply: {
        layout: { textAlign: "center", fontWeight: 700, fontSize: 16, paddingX: 18, paddingY: 12 },
        paint: {
          nodeFill: "#eaddff",
          nodeFillSelected: "#d0bcff",
          text: "#21005d"
        },
        incomingEdge: { strokeColor: "#6750a4", strokeWidth: 2.5 }
      }
    },
    {
      id: "m3-depth-1",
      priority: 10,
      when: { kind: "depth", depth: 1 },
      apply: {
        layout: { fontWeight: 600 },
        paint: { nodeFill: "#e8def8", text: "#1d192b" },
        incomingEdge: { strokeColor: "#625b71" }
      }
    },
    {
      id: "m3-depth-2",
      priority: 10,
      when: { kind: "depth", depth: 2 },
      apply: {
        paint: { nodeFill: "#ffd8e4", text: "#31111d" },
        incomingEdge: { strokeColor: "#7d5260" }
      }
    },
    {
      id: "m3-depth-3plus",
      priority: 10,
      when: { kind: "depthRange", minDepth: 3 },
      apply: { incomingEdge: { strokeWidth: 1.75 } }
    }
  ];
  const rulesDark = [
    {
      id: "m3-root",
      priority: 10,
      when: { kind: "depth", depth: 0 },
      apply: {
        layout: { textAlign: "center", fontWeight: 700, fontSize: 16, paddingX: 18, paddingY: 12 },
        paint: {
          nodeFill: "#4f378b",
          nodeFillSelected: "#6750a4",
          text: "#fef7ff"
        },
        incomingEdge: { strokeColor: "#d0bcff", strokeWidth: 2.5 }
      }
    },
    {
      id: "m3-depth-1",
      priority: 10,
      when: { kind: "depth", depth: 1 },
      apply: {
        layout: { fontWeight: 600 },
        paint: { nodeFill: "#332d41", text: "#e6e1e5" },
        incomingEdge: { strokeColor: "#cbc2db" }
      }
    },
    {
      id: "m3-depth-2",
      priority: 10,
      when: { kind: "depth", depth: 2 },
      apply: {
        paint: { nodeFill: "#492532", text: "#fef7ff" },
        incomingEdge: { strokeColor: "#efb8c8" }
      }
    },
    {
      id: "m3-depth-3plus",
      priority: 10,
      when: { kind: "depthRange", minDepth: 3 },
      apply: { incomingEdge: { strokeWidth: 1.75 } }
    }
  ];
  theme.variants.light.rules = { nodeRules: rulesLight };
  theme.variants.dark.rules = { nodeRules: rulesDark };
  return theme;
})();

// ../themes/src/themes/material-3-rounded-orthogonal-aqua.ts
var material3RoundedOrthogonalAquaTheme = {
  "schemaVersion": 1,
  "id": "kmind-material-3-rounded-orthogonal-aqua",
  "name": "Material 3 \xB7 Rounded Orthogonal \xB7 Aqua",
  "variants": {
    "light": {
      "tokens": {
        "layout": {
          "fontFamily": "ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif",
          "fontSize": 14,
          "fontWeight": 450,
          "lineHeight": 1.45,
          "textAlign": "left",
          "paddingX": 14,
          "paddingY": 10,
          "nodeMinWidth": 60,
          "nodeMinHeight": 40
        },
        "paint": {
          "bg": "#f2fffd",
          "panel": "#ffffff",
          "text": "#1a1f1e",
          "muted": "#3f4947",
          "border": "#cfe7e2",
          "nodeFill": "#e8f6f2",
          "nodeFillSelected": "#b9ebe3",
          "nodeStroke": "transparent",
          "nodeStrokeSelected": "#006a60",
          "edgeStroke": "#6b7a76",
          "relationStroke": "#8f4c00",
          "relationStrokeSelected": "#ba1a1a",
          "summaryStroke": "#b7d7d1"
        }
      },
      "edges": {
        "strokeWidth": 4,
        "cap": "round",
        "join": "round",
        "routeType": "orthogonal-rounded"
      },
      "relations": {
        "strokeWidth": 2,
        "cap": "round",
        "join": "round"
      },
      "nodeShape": {
        "type": "rounded-rect",
        "radius": 16,
        "strokeWidth": 0
      },
      "rainbow": {
        "enabled": false,
        "palette": [
          "#006a60",
          "#14b8a6",
          "#06b6d4",
          "#0ea5e9",
          "#60a5fa",
          "#f59e0b",
          "#fb7185",
          "#a78bfa"
        ]
      },
      "background": {
        "color": "#f2fffd"
      },
      "rules": {
        "nodeRules": [
          {
            "id": "m3-root",
            "priority": 10,
            "when": {
              "kind": "depth",
              "depth": 0
            },
            "apply": {
              "layout": {
                "textAlign": "center",
                "fontWeight": 700,
                "fontSize": 24,
                "paddingX": 18,
                "paddingY": 12
              },
              "paint": {
                "nodeFill": "#b9ebe3",
                "nodeFillSelected": "#80d5c9",
                "text": "#00201d"
              },
              "incomingEdge": {
                "strokeColor": "#006a60",
                "strokeWidth": 2.5
              }
            }
          },
          {
            "id": "m3-depth-1",
            "priority": 10,
            "when": {
              "kind": "depth",
              "depth": 1
            },
            "apply": {
              "layout": {
                "fontWeight": 600,
                "fontSize": 18
              },
              "paint": {
                "nodeFill": "#cfe7e2",
                "text": "#10201e"
              },
              "incomingEdge": {
                "strokeColor": "#3f5f5a",
                "routeType": "center-quadratic"
              }
            }
          },
          {
            "id": "m3-depth-2",
            "priority": 10,
            "when": {
              "kind": "depth",
              "depth": 2
            },
            "apply": {
              "paint": {
                "nodeFill": "#ffddb5",
                "text": "#2b1600"
              },
              "incomingEdge": {
                "strokeColor": "#8f4c00"
              }
            }
          },
          {
            "id": "m3-depth-3plus",
            "priority": 10,
            "when": {
              "kind": "depthRange",
              "minDepth": 3
            },
            "apply": {
              "incomingEdge": {
                "strokeWidth": 1.75
              }
            }
          }
        ]
      }
    },
    "dark": {
      "tokens": {
        "layout": {
          "fontFamily": "ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif",
          "fontSize": 14,
          "fontWeight": 450,
          "lineHeight": 1.45,
          "textAlign": "left",
          "paddingX": 14,
          "paddingY": 10,
          "nodeMinWidth": 60,
          "nodeMinHeight": 40
        },
        "paint": {
          "bg": "#0e1413",
          "panel": "#151d1c",
          "text": "#dce5e3",
          "muted": "#b7d7d1",
          "border": "rgba(183, 215, 209, 0.22)",
          "nodeFill": "#1a2221",
          "nodeFillSelected": "#00504a",
          "nodeStroke": "transparent",
          "nodeStrokeSelected": "#b9ebe3",
          "edgeStroke": "#8ea3a0",
          "relationStroke": "#ffb86c",
          "relationStrokeSelected": "#ffb4ab",
          "summaryStroke": "#3f4947"
        }
      },
      "edges": {
        "strokeWidth": 4,
        "cap": "round",
        "join": "round",
        "routeType": "orthogonal-rounded"
      },
      "relations": {
        "strokeWidth": 2,
        "cap": "round",
        "join": "round"
      },
      "nodeShape": {
        "type": "rounded-rect",
        "radius": 16,
        "strokeWidth": 0
      },
      "rainbow": {
        "enabled": false,
        "palette": [
          "#006a60",
          "#14b8a6",
          "#06b6d4",
          "#0ea5e9",
          "#60a5fa",
          "#f59e0b",
          "#fb7185",
          "#a78bfa"
        ]
      },
      "background": {
        "color": "#0e1413"
      },
      "rules": {
        "nodeRules": [
          {
            "id": "m3-root",
            "priority": 10,
            "when": {
              "kind": "depth",
              "depth": 0
            },
            "apply": {
              "layout": {
                "textAlign": "center",
                "fontWeight": 700,
                "fontSize": 24,
                "paddingX": 18,
                "paddingY": 12
              },
              "paint": {
                "nodeFill": "#00504a",
                "nodeFillSelected": "#006a60",
                "text": "#f2fffd"
              },
              "incomingEdge": {
                "strokeColor": "#b9ebe3",
                "strokeWidth": 2.5
              }
            }
          },
          {
            "id": "m3-depth-1",
            "priority": 10,
            "when": {
              "kind": "depth",
              "depth": 1
            },
            "apply": {
              "layout": {
                "fontWeight": 600,
                "fontSize": 18
              },
              "paint": {
                "nodeFill": "#293231",
                "text": "#dce5e3"
              },
              "incomingEdge": {
                "strokeColor": "#a8d1cb",
                "routeType": "center-quadratic"
              }
            }
          },
          {
            "id": "m3-depth-2",
            "priority": 10,
            "when": {
              "kind": "depth",
              "depth": 2
            },
            "apply": {
              "paint": {
                "nodeFill": "#4a2a00",
                "text": "#ffe8cc"
              },
              "incomingEdge": {
                "strokeColor": "#ffb86c"
              }
            }
          },
          {
            "id": "m3-depth-3plus",
            "priority": 10,
            "when": {
              "kind": "depthRange",
              "minDepth": 3
            },
            "apply": {
              "incomingEdge": {
                "strokeWidth": 1.75
              }
            }
          }
        ]
      }
    }
  }
};

// ../themes/src/themes/material-3-rounded-orthogonal-citrus.ts
var material3RoundedOrthogonalCitrusTheme = {
  "schemaVersion": 1,
  "id": "kmind-material-3-rounded-orthogonal-citrus",
  "name": "Material 3 \xB7 Rounded Orthogonal \xB7 Citrus",
  "variants": {
    "light": {
      "tokens": {
        "layout": {
          "fontFamily": "ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif",
          "fontSize": 14,
          "fontWeight": 450,
          "lineHeight": 1.45,
          "textAlign": "left",
          "paddingX": 14,
          "paddingY": 10,
          "nodeMinWidth": 60,
          "nodeMinHeight": 40
        },
        "paint": {
          "bg": "#fff8f1",
          "panel": "#ffffff",
          "text": "#201a13",
          "muted": "#51443a",
          "border": "#f2dccc",
          "nodeFill": "#fff1e6",
          "nodeFillSelected": "#ffddb5",
          "nodeStroke": "transparent",
          "nodeStrokeSelected": "#8f4c00",
          "edgeStroke": "#857468",
          "relationStroke": "#006a6a",
          "relationStrokeSelected": "#ba1a1a",
          "summaryStroke": "#d7c2b3"
        }
      },
      "edges": {
        "strokeWidth": 4,
        "cap": "round",
        "join": "round",
        "routeType": "orthogonal-rounded"
      },
      "relations": {
        "strokeWidth": 2,
        "cap": "round",
        "join": "round"
      },
      "nodeShape": {
        "type": "rounded-rect",
        "radius": 16,
        "strokeWidth": 0
      },
      "rainbow": {
        "enabled": false,
        "palette": [
          "#8f4c00",
          "#f59e0b",
          "#f97316",
          "#ef4444",
          "#fb7185",
          "#a78bfa",
          "#0ea5e9",
          "#14b8a6"
        ]
      },
      "background": {
        "color": "#fff8f1"
      },
      "rules": {
        "nodeRules": [
          {
            "id": "m3-root",
            "priority": 10,
            "when": {
              "kind": "depth",
              "depth": 0
            },
            "apply": {
              "layout": {
                "textAlign": "center",
                "fontWeight": 700,
                "fontSize": 24,
                "paddingX": 18,
                "paddingY": 12
              },
              "paint": {
                "nodeFill": "#ffddb5",
                "nodeFillSelected": "#ffb86c",
                "text": "#2b1600"
              },
              "incomingEdge": {
                "strokeColor": "#8f4c00",
                "strokeWidth": 2.5
              }
            }
          },
          {
            "id": "m3-depth-1",
            "priority": 10,
            "when": {
              "kind": "depth",
              "depth": 1
            },
            "apply": {
              "layout": {
                "fontWeight": 600,
                "fontSize": 18
              },
              "paint": {
                "nodeFill": "#f2dccc",
                "text": "#231a12"
              },
              "incomingEdge": {
                "strokeColor": "#7a5a43",
                "routeType": "center-quadratic"
              }
            }
          },
          {
            "id": "m3-depth-2",
            "priority": 10,
            "when": {
              "kind": "depth",
              "depth": 2
            },
            "apply": {
              "paint": {
                "nodeFill": "#d6f5ff",
                "text": "#002022"
              },
              "incomingEdge": {
                "strokeColor": "#006a6a"
              }
            }
          },
          {
            "id": "m3-depth-3plus",
            "priority": 10,
            "when": {
              "kind": "depthRange",
              "minDepth": 3
            },
            "apply": {
              "incomingEdge": {
                "strokeWidth": 1.75
              }
            }
          }
        ]
      }
    },
    "dark": {
      "tokens": {
        "layout": {
          "fontFamily": "ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif",
          "fontSize": 14,
          "fontWeight": 450,
          "lineHeight": 1.45,
          "textAlign": "left",
          "paddingX": 14,
          "paddingY": 10,
          "nodeMinWidth": 60,
          "nodeMinHeight": 40
        },
        "paint": {
          "bg": "#1a120b",
          "panel": "#241a12",
          "text": "#f2dfd2",
          "muted": "#d7c2b3",
          "border": "rgba(215, 194, 179, 0.22)",
          "nodeFill": "#2a1f16",
          "nodeFillSelected": "#6b3b00",
          "nodeStroke": "transparent",
          "nodeStrokeSelected": "#ffddb5",
          "edgeStroke": "#a39184",
          "relationStroke": "#4fd8eb",
          "relationStrokeSelected": "#ffb4ab",
          "summaryStroke": "#51443a"
        }
      },
      "edges": {
        "strokeWidth": 4,
        "cap": "round",
        "join": "round",
        "routeType": "orthogonal-rounded"
      },
      "relations": {
        "strokeWidth": 2,
        "cap": "round",
        "join": "round"
      },
      "nodeShape": {
        "type": "rounded-rect",
        "radius": 16,
        "strokeWidth": 0
      },
      "rainbow": {
        "enabled": false,
        "palette": [
          "#8f4c00",
          "#f59e0b",
          "#f97316",
          "#ef4444",
          "#fb7185",
          "#a78bfa",
          "#0ea5e9",
          "#14b8a6"
        ]
      },
      "background": {
        "color": "#1a120b"
      },
      "rules": {
        "nodeRules": [
          {
            "id": "m3-root",
            "priority": 10,
            "when": {
              "kind": "depth",
              "depth": 0
            },
            "apply": {
              "layout": {
                "textAlign": "center",
                "fontWeight": 700,
                "fontSize": 24,
                "paddingX": 18,
                "paddingY": 12
              },
              "paint": {
                "nodeFill": "#6b3b00",
                "nodeFillSelected": "#8f4c00",
                "text": "#fff8f1"
              },
              "incomingEdge": {
                "strokeColor": "#ffddb5",
                "strokeWidth": 2.5
              }
            }
          },
          {
            "id": "m3-depth-1",
            "priority": 10,
            "when": {
              "kind": "depth",
              "depth": 1
            },
            "apply": {
              "layout": {
                "fontWeight": 600,
                "fontSize": 18
              },
              "paint": {
                "nodeFill": "#3a2b21",
                "text": "#f2dfd2"
              },
              "incomingEdge": {
                "strokeColor": "#e5c4a5",
                "routeType": "center-quadratic"
              }
            }
          },
          {
            "id": "m3-depth-2",
            "priority": 10,
            "when": {
              "kind": "depth",
              "depth": 2
            },
            "apply": {
              "paint": {
                "nodeFill": "#00363a",
                "text": "#e1f4f5"
              },
              "incomingEdge": {
                "strokeColor": "#4fd8eb"
              }
            }
          },
          {
            "id": "m3-depth-3plus",
            "priority": 10,
            "when": {
              "kind": "depthRange",
              "minDepth": 3
            },
            "apply": {
              "incomingEdge": {
                "strokeWidth": 1.75
              }
            }
          }
        ]
      }
    }
  }
};

// ../themes/src/themes/material-3-rounded-orthogonal-forest.ts
var material3RoundedOrthogonalForestTheme = {
  "schemaVersion": 1,
  "id": "kmind-material-3-rounded-orthogonal-forest",
  "name": "Material 3 \xB7 Rounded Orthogonal \xB7 Forest",
  "variants": {
    "light": {
      "tokens": {
        "layout": {
          "fontFamily": "ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif",
          "fontSize": 14,
          "fontWeight": 450,
          "lineHeight": 1.45,
          "textAlign": "left",
          "paddingX": 14,
          "paddingY": 10,
          "nodeMinWidth": 60,
          "nodeMinHeight": 40
        },
        "paint": {
          "bg": "#f5fff7",
          "panel": "#ffffff",
          "text": "#1b1f1b",
          "muted": "#444a44",
          "border": "#dbe5db",
          "nodeFill": "#eef7ee",
          "nodeFillSelected": "#cfe9d2",
          "nodeStroke": "transparent",
          "nodeStrokeSelected": "#0f6d2b",
          "edgeStroke": "#6f7a6f",
          "relationStroke": "#006a60",
          "relationStrokeSelected": "#ba1a1a",
          "summaryStroke": "#c4cec3"
        }
      },
      "edges": {
        "strokeWidth": 4,
        "cap": "round",
        "join": "round",
        "routeType": "orthogonal-rounded"
      },
      "relations": {
        "strokeWidth": 2,
        "cap": "round",
        "join": "round"
      },
      "nodeShape": {
        "type": "rounded-rect",
        "radius": 16,
        "strokeWidth": 0
      },
      "rainbow": {
        "enabled": false,
        "palette": [
          "#0f6d2b",
          "#22c55e",
          "#14b8a6",
          "#06b6d4",
          "#60a5fa",
          "#f59e0b",
          "#fb7185",
          "#a78bfa"
        ]
      },
      "background": {
        "color": "#f5fff7"
      },
      "rules": {
        "nodeRules": [
          {
            "id": "m3-root",
            "priority": 10,
            "when": {
              "kind": "depth",
              "depth": 0
            },
            "apply": {
              "layout": {
                "textAlign": "center",
                "fontWeight": 700,
                "fontSize": 24,
                "paddingX": 18,
                "paddingY": 12
              },
              "paint": {
                "nodeFill": "#cfe9d2",
                "nodeFillSelected": "#a3d6a8",
                "text": "#00210f"
              },
              "incomingEdge": {
                "strokeColor": "#0f6d2b",
                "strokeWidth": 2.5
              }
            }
          },
          {
            "id": "m3-depth-1",
            "priority": 10,
            "when": {
              "kind": "depth",
              "depth": 1
            },
            "apply": {
              "layout": {
                "fontWeight": 600,
                "fontSize": 18
              },
              "paint": {
                "nodeFill": "#dcebdd",
                "text": "#132016"
              },
              "incomingEdge": {
                "strokeColor": "#3d5e3f",
                "routeType": "center-quadratic"
              }
            }
          },
          {
            "id": "m3-depth-2",
            "priority": 10,
            "when": {
              "kind": "depth",
              "depth": 2
            },
            "apply": {
              "paint": {
                "nodeFill": "#ffe8cc",
                "text": "#2b1600"
              },
              "incomingEdge": {
                "strokeColor": "#8c5000"
              }
            }
          },
          {
            "id": "m3-depth-3plus",
            "priority": 10,
            "when": {
              "kind": "depthRange",
              "minDepth": 3
            },
            "apply": {
              "incomingEdge": {
                "strokeWidth": 1.75
              }
            }
          }
        ]
      }
    },
    "dark": {
      "tokens": {
        "layout": {
          "fontFamily": "ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif",
          "fontSize": 14,
          "fontWeight": 450,
          "lineHeight": 1.45,
          "textAlign": "left",
          "paddingX": 14,
          "paddingY": 10,
          "nodeMinWidth": 60,
          "nodeMinHeight": 40
        },
        "paint": {
          "bg": "#0f1410",
          "panel": "#171d18",
          "text": "#e0e4dd",
          "muted": "#c4cec3",
          "border": "rgba(196, 206, 195, 0.22)",
          "nodeFill": "#1a221b",
          "nodeFillSelected": "#1b5e20",
          "nodeStroke": "transparent",
          "nodeStrokeSelected": "#a3d6a8",
          "edgeStroke": "#909a90",
          "relationStroke": "#4fd8c7",
          "relationStrokeSelected": "#ffb4ab",
          "summaryStroke": "#444a44"
        }
      },
      "edges": {
        "strokeWidth": 4,
        "cap": "round",
        "join": "round",
        "routeType": "orthogonal-rounded"
      },
      "relations": {
        "strokeWidth": 2,
        "cap": "round",
        "join": "round"
      },
      "nodeShape": {
        "type": "rounded-rect",
        "radius": 16,
        "strokeWidth": 0
      },
      "rainbow": {
        "enabled": false,
        "palette": [
          "#0f6d2b",
          "#22c55e",
          "#14b8a6",
          "#06b6d4",
          "#60a5fa",
          "#f59e0b",
          "#fb7185",
          "#a78bfa"
        ]
      },
      "background": {
        "color": "#0f1410"
      },
      "rules": {
        "nodeRules": [
          {
            "id": "m3-root",
            "priority": 10,
            "when": {
              "kind": "depth",
              "depth": 0
            },
            "apply": {
              "layout": {
                "textAlign": "center",
                "fontWeight": 700,
                "fontSize": 24,
                "paddingX": 18,
                "paddingY": 12
              },
              "paint": {
                "nodeFill": "#1b5e20",
                "nodeFillSelected": "#0f6d2b",
                "text": "#f5fff7"
              },
              "incomingEdge": {
                "strokeColor": "#a3d6a8",
                "strokeWidth": 2.5
              }
            }
          },
          {
            "id": "m3-depth-1",
            "priority": 10,
            "when": {
              "kind": "depth",
              "depth": 1
            },
            "apply": {
              "layout": {
                "fontWeight": 600,
                "fontSize": 18
              },
              "paint": {
                "nodeFill": "#2a322b",
                "text": "#e0e4dd"
              },
              "incomingEdge": {
                "strokeColor": "#b1d9b3",
                "routeType": "center-quadratic"
              }
            }
          },
          {
            "id": "m3-depth-2",
            "priority": 10,
            "when": {
              "kind": "depth",
              "depth": 2
            },
            "apply": {
              "paint": {
                "nodeFill": "#4a2a00",
                "text": "#ffe8cc"
              },
              "incomingEdge": {
                "strokeColor": "#ffb86c"
              }
            }
          },
          {
            "id": "m3-depth-3plus",
            "priority": 10,
            "when": {
              "kind": "depthRange",
              "minDepth": 3
            },
            "apply": {
              "incomingEdge": {
                "strokeWidth": 1.75
              }
            }
          }
        ]
      }
    }
  }
};

// ../themes/src/themes/material-3-rounded-orthogonal-ocean.ts
var material3RoundedOrthogonalOceanTheme = {
  "schemaVersion": 1,
  "id": "kmind-material-3-rounded-orthogonal-ocean",
  "name": "Material 3 \xB7 Rounded Orthogonal \xB7 Ocean",
  "variants": {
    "light": {
      "tokens": {
        "layout": {
          "fontFamily": "ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif",
          "fontSize": 14,
          "fontWeight": 450,
          "lineHeight": 1.45,
          "textAlign": "left",
          "paddingX": 14,
          "paddingY": 10,
          "nodeMinWidth": 60,
          "nodeMinHeight": 40
        },
        "paint": {
          "bg": "#f6f9ff",
          "panel": "#ffffff",
          "text": "#1a1b1f",
          "muted": "#44474f",
          "border": "#dfe3eb",
          "nodeFill": "#eef2fb",
          "nodeFillSelected": "#d7e3ff",
          "nodeStroke": "transparent",
          "nodeStrokeSelected": "#1b5fa7",
          "edgeStroke": "#6c778a",
          "relationStroke": "#006a6a",
          "relationStrokeSelected": "#ba1a1a",
          "summaryStroke": "#c3c7cf"
        }
      },
      "edges": {
        "strokeWidth": 4,
        "cap": "round",
        "join": "round",
        "routeType": "orthogonal-rounded"
      },
      "relations": {
        "strokeWidth": 2,
        "cap": "round",
        "join": "round"
      },
      "nodeShape": {
        "type": "rounded-rect",
        "radius": 16,
        "strokeWidth": 0
      },
      "rainbow": {
        "enabled": false,
        "palette": [
          "#1b5fa7",
          "#2f6fe3",
          "#0ea5e9",
          "#14b8a6",
          "#22c55e",
          "#f59e0b",
          "#fb7185",
          "#a78bfa"
        ]
      },
      "background": {
        "color": "#f6f9ff"
      },
      "rules": {
        "nodeRules": [
          {
            "id": "m3-root",
            "priority": 10,
            "when": {
              "kind": "depth",
              "depth": 0
            },
            "apply": {
              "layout": {
                "textAlign": "center",
                "fontWeight": 700,
                "fontSize": 24,
                "paddingX": 18,
                "paddingY": 12
              },
              "paint": {
                "nodeFill": "#d7e3ff",
                "nodeFillSelected": "#aec6ff",
                "text": "#001b3f"
              },
              "incomingEdge": {
                "strokeColor": "#1b5fa7",
                "strokeWidth": 2.5
              }
            }
          },
          {
            "id": "m3-depth-1",
            "priority": 10,
            "when": {
              "kind": "depth",
              "depth": 1
            },
            "apply": {
              "layout": {
                "fontWeight": 600,
                "fontSize": 18
              },
              "paint": {
                "nodeFill": "#d7e3f8",
                "text": "#1c1e24"
              },
              "incomingEdge": {
                "strokeColor": "#415f91",
                "routeType": "center-quadratic"
              }
            }
          },
          {
            "id": "m3-depth-2",
            "priority": 10,
            "when": {
              "kind": "depth",
              "depth": 2
            },
            "apply": {
              "paint": {
                "nodeFill": "#cfe9ff",
                "text": "#002022"
              },
              "incomingEdge": {
                "strokeColor": "#006a6a"
              }
            }
          },
          {
            "id": "m3-depth-3plus",
            "priority": 10,
            "when": {
              "kind": "depthRange",
              "minDepth": 3
            },
            "apply": {
              "incomingEdge": {
                "strokeWidth": 1.75
              }
            }
          }
        ]
      }
    },
    "dark": {
      "tokens": {
        "layout": {
          "fontFamily": "ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif",
          "fontSize": 14,
          "fontWeight": 450,
          "lineHeight": 1.45,
          "textAlign": "left",
          "paddingX": 14,
          "paddingY": 10,
          "nodeMinWidth": 60,
          "nodeMinHeight": 40
        },
        "paint": {
          "bg": "#0f1117",
          "panel": "#161b22",
          "text": "#e1e2e6",
          "muted": "#c3c7cf",
          "border": "rgba(195, 199, 207, 0.22)",
          "nodeFill": "#1a1f27",
          "nodeFillSelected": "#0e4b8a",
          "nodeStroke": "transparent",
          "nodeStrokeSelected": "#d7e3ff",
          "edgeStroke": "#8f98a7",
          "relationStroke": "#4fd8eb",
          "relationStrokeSelected": "#ffb4ab",
          "summaryStroke": "#44474f"
        }
      },
      "edges": {
        "strokeWidth": 4,
        "cap": "round",
        "join": "round",
        "routeType": "orthogonal-rounded"
      },
      "relations": {
        "strokeWidth": 2,
        "cap": "round",
        "join": "round"
      },
      "nodeShape": {
        "type": "rounded-rect",
        "radius": 16,
        "strokeWidth": 0
      },
      "rainbow": {
        "enabled": false,
        "palette": [
          "#1b5fa7",
          "#2f6fe3",
          "#0ea5e9",
          "#14b8a6",
          "#22c55e",
          "#f59e0b",
          "#fb7185",
          "#a78bfa"
        ]
      },
      "background": {
        "color": "#0f1117"
      },
      "rules": {
        "nodeRules": [
          {
            "id": "m3-root",
            "priority": 10,
            "when": {
              "kind": "depth",
              "depth": 0
            },
            "apply": {
              "layout": {
                "textAlign": "center",
                "fontWeight": 700,
                "fontSize": 24,
                "paddingX": 18,
                "paddingY": 12
              },
              "paint": {
                "nodeFill": "#0e4b8a",
                "nodeFillSelected": "#1b5fa7",
                "text": "#f6f9ff"
              },
              "incomingEdge": {
                "strokeColor": "#d7e3ff",
                "strokeWidth": 2.5
              }
            }
          },
          {
            "id": "m3-depth-1",
            "priority": 10,
            "when": {
              "kind": "depth",
              "depth": 1
            },
            "apply": {
              "layout": {
                "fontWeight": 600,
                "fontSize": 18
              },
              "paint": {
                "nodeFill": "#2a3140",
                "text": "#e1e2e6"
              },
              "incomingEdge": {
                "strokeColor": "#b0c6ff",
                "routeType": "center-quadratic"
              }
            }
          },
          {
            "id": "m3-depth-2",
            "priority": 10,
            "when": {
              "kind": "depth",
              "depth": 2
            },
            "apply": {
              "paint": {
                "nodeFill": "#00363a",
                "text": "#e1f4f5"
              },
              "incomingEdge": {
                "strokeColor": "#4fd8eb"
              }
            }
          },
          {
            "id": "m3-depth-3plus",
            "priority": 10,
            "when": {
              "kind": "depthRange",
              "minDepth": 3
            },
            "apply": {
              "incomingEdge": {
                "strokeWidth": 1.75
              }
            }
          }
        ]
      }
    }
  }
};

// ../themes/src/themes/material-3-rounded-orthogonal-rose.ts
var material3RoundedOrthogonalRoseTheme = {
  "schemaVersion": 1,
  "id": "kmind-material-3-rounded-orthogonal-rose",
  "name": "Material 3 \xB7 Rounded Orthogonal \xB7 Rose",
  "variants": {
    "light": {
      "tokens": {
        "layout": {
          "fontFamily": "ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif",
          "fontSize": 14,
          "fontWeight": 450,
          "lineHeight": 1.45,
          "textAlign": "left",
          "paddingX": 14,
          "paddingY": 10,
          "nodeMinWidth": 60,
          "nodeMinHeight": 40
        },
        "paint": {
          "bg": "#fff7f9",
          "panel": "#ffffff",
          "text": "#201a1b",
          "muted": "#514345",
          "border": "#f2dce0",
          "nodeFill": "#fff0f3",
          "nodeFillSelected": "#ffd9e0",
          "nodeStroke": "transparent",
          "nodeStrokeSelected": "#b0003a",
          "edgeStroke": "#857376",
          "relationStroke": "#006a6a",
          "relationStrokeSelected": "#ba1a1a",
          "summaryStroke": "#d7c2c6"
        }
      },
      "edges": {
        "strokeWidth": 4,
        "cap": "round",
        "join": "round",
        "routeType": "orthogonal-rounded"
      },
      "relations": {
        "strokeWidth": 2,
        "cap": "round",
        "join": "round"
      },
      "nodeShape": {
        "type": "rounded-rect",
        "radius": 16,
        "strokeWidth": 0
      },
      "rainbow": {
        "enabled": false,
        "palette": [
          "#b0003a",
          "#fb7185",
          "#ef4444",
          "#f59e0b",
          "#22c55e",
          "#14b8a6",
          "#0ea5e9",
          "#a78bfa"
        ]
      },
      "background": {
        "color": "#fff7f9"
      },
      "rules": {
        "nodeRules": [
          {
            "id": "m3-root",
            "priority": 10,
            "when": {
              "kind": "depth",
              "depth": 0
            },
            "apply": {
              "layout": {
                "textAlign": "center",
                "fontWeight": 700,
                "fontSize": 24,
                "paddingX": 18,
                "paddingY": 12
              },
              "paint": {
                "nodeFill": "#ffd9e0",
                "nodeFillSelected": "#ffb1c3",
                "text": "#3a0713"
              },
              "incomingEdge": {
                "strokeColor": "#b0003a",
                "strokeWidth": 2.5
              }
            }
          },
          {
            "id": "m3-depth-1",
            "priority": 10,
            "when": {
              "kind": "depth",
              "depth": 1
            },
            "apply": {
              "layout": {
                "fontWeight": 600,
                "fontSize": 18
              },
              "paint": {
                "nodeFill": "#f2dce0",
                "text": "#231a1b"
              },
              "incomingEdge": {
                "strokeColor": "#7a4a56",
                "routeType": "center-quadratic"
              }
            }
          },
          {
            "id": "m3-depth-2",
            "priority": 10,
            "when": {
              "kind": "depth",
              "depth": 2
            },
            "apply": {
              "paint": {
                "nodeFill": "#eaddff",
                "text": "#21005d"
              },
              "incomingEdge": {
                "strokeColor": "#6750a4"
              }
            }
          },
          {
            "id": "m3-depth-3plus",
            "priority": 10,
            "when": {
              "kind": "depthRange",
              "minDepth": 3
            },
            "apply": {
              "incomingEdge": {
                "strokeWidth": 1.75
              }
            }
          }
        ]
      }
    },
    "dark": {
      "tokens": {
        "layout": {
          "fontFamily": "ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif",
          "fontSize": 14,
          "fontWeight": 450,
          "lineHeight": 1.45,
          "textAlign": "left",
          "paddingX": 14,
          "paddingY": 10,
          "nodeMinWidth": 60,
          "nodeMinHeight": 40
        },
        "paint": {
          "bg": "#1a1113",
          "panel": "#241a1c",
          "text": "#f2dfe2",
          "muted": "#d7c2c6",
          "border": "rgba(215, 194, 198, 0.22)",
          "nodeFill": "#2a1f21",
          "nodeFillSelected": "#8c0030",
          "nodeStroke": "transparent",
          "nodeStrokeSelected": "#ffd9e0",
          "edgeStroke": "#a39195",
          "relationStroke": "#4fd8eb",
          "relationStrokeSelected": "#ffb4ab",
          "summaryStroke": "#514345"
        }
      },
      "edges": {
        "strokeWidth": 4,
        "cap": "round",
        "join": "round",
        "routeType": "orthogonal-rounded"
      },
      "relations": {
        "strokeWidth": 2,
        "cap": "round",
        "join": "round"
      },
      "nodeShape": {
        "type": "rounded-rect",
        "radius": 16,
        "strokeWidth": 0
      },
      "rainbow": {
        "enabled": false,
        "palette": [
          "#b0003a",
          "#fb7185",
          "#ef4444",
          "#f59e0b",
          "#22c55e",
          "#14b8a6",
          "#0ea5e9",
          "#a78bfa"
        ]
      },
      "background": {
        "color": "#1a1113"
      },
      "rules": {
        "nodeRules": [
          {
            "id": "m3-root",
            "priority": 10,
            "when": {
              "kind": "depth",
              "depth": 0
            },
            "apply": {
              "layout": {
                "textAlign": "center",
                "fontWeight": 700,
                "fontSize": 24,
                "paddingX": 18,
                "paddingY": 12
              },
              "paint": {
                "nodeFill": "#8c0030",
                "nodeFillSelected": "#b0003a",
                "text": "#fff7f9"
              },
              "incomingEdge": {
                "strokeColor": "#ffd9e0",
                "strokeWidth": 2.5
              }
            }
          },
          {
            "id": "m3-depth-1",
            "priority": 10,
            "when": {
              "kind": "depth",
              "depth": 1
            },
            "apply": {
              "layout": {
                "fontWeight": 600,
                "fontSize": 18
              },
              "paint": {
                "nodeFill": "#3a2b2d",
                "text": "#f2dfe2"
              },
              "incomingEdge": {
                "strokeColor": "#f0b6c1",
                "routeType": "center-quadratic"
              }
            }
          },
          {
            "id": "m3-depth-2",
            "priority": 10,
            "when": {
              "kind": "depth",
              "depth": 2
            },
            "apply": {
              "paint": {
                "nodeFill": "#4f378b",
                "text": "#fef7ff"
              },
              "incomingEdge": {
                "strokeColor": "#d0bcff"
              }
            }
          },
          {
            "id": "m3-depth-3plus",
            "priority": 10,
            "when": {
              "kind": "depthRange",
              "minDepth": 3
            },
            "apply": {
              "incomingEdge": {
                "strokeWidth": 1.75
              }
            }
          }
        ]
      }
    }
  }
};

// ../themes/src/themes/material-3-rounded-orthogonal-violet.ts
var material3RoundedOrthogonalVioletTheme = {
  "schemaVersion": 1,
  "id": "kmind-material-3-rounded-orthogonal-violet",
  "name": "Material 3 \xB7 Rounded Orthogonal \xB7 Violet",
  "variants": {
    "light": {
      "tokens": {
        "layout": {
          "fontFamily": "ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif",
          "fontSize": 14,
          "fontWeight": 450,
          "lineHeight": 1.45,
          "textAlign": "left",
          "paddingX": 14,
          "paddingY": 10,
          "nodeMinWidth": 60,
          "nodeMinHeight": 40
        },
        "paint": {
          "bg": "#fef7ff",
          "panel": "#ffffff",
          "text": "#1c1b1f",
          "muted": "#49454f",
          "border": "#e7e0ec",
          "nodeFill": "#f3edf7",
          "nodeFillSelected": "#eaddff",
          "nodeStroke": "transparent",
          "nodeStrokeSelected": "#6750a4",
          "edgeStroke": "#79747e",
          "relationStroke": "#7d5260",
          "relationStrokeSelected": "#b3261e",
          "summaryStroke": "#cac4d0"
        }
      },
      "edges": {
        "strokeWidth": 4,
        "cap": "round",
        "join": "round",
        "routeType": "orthogonal-rounded"
      },
      "relations": {
        "strokeWidth": 2,
        "cap": "round",
        "join": "round"
      },
      "nodeShape": {
        "type": "rounded-rect",
        "radius": 16,
        "strokeWidth": 0
      },
      "rainbow": {
        "enabled": false,
        "palette": [
          "#ef4444",
          "#f97316",
          "#eab308",
          "#22c55e",
          "#06b6d4",
          "#3b82f6",
          "#8b5cf6",
          "#ec4899"
        ]
      },
      "background": {
        "color": "#fef7ff"
      },
      "rules": {
        "nodeRules": [
          {
            "id": "m3-root",
            "priority": 10,
            "when": {
              "kind": "depth",
              "depth": 0
            },
            "apply": {
              "layout": {
                "textAlign": "center",
                "fontWeight": 700,
                "fontSize": 24,
                "paddingX": 18,
                "paddingY": 12
              },
              "paint": {
                "nodeFill": "#eaddff",
                "nodeFillSelected": "#d0bcff",
                "text": "#21005d"
              },
              "incomingEdge": {
                "strokeColor": "#6750a4",
                "strokeWidth": 2.5
              }
            }
          },
          {
            "id": "m3-depth-1",
            "priority": 10,
            "when": {
              "kind": "depth",
              "depth": 1
            },
            "apply": {
              "layout": {
                "fontWeight": 600,
                "fontSize": 18
              },
              "paint": {
                "nodeFill": "#e8def8",
                "text": "#1d192b"
              },
              "incomingEdge": {
                "strokeColor": "#625b71",
                "routeType": "center-quadratic"
              }
            }
          },
          {
            "id": "m3-depth-2",
            "priority": 10,
            "when": {
              "kind": "depth",
              "depth": 2
            },
            "apply": {
              "paint": {
                "nodeFill": "#ffd8e4",
                "text": "#31111d"
              },
              "incomingEdge": {
                "strokeColor": "#7d5260"
              }
            }
          }
        ]
      }
    },
    "dark": {
      "tokens": {
        "layout": {
          "fontFamily": "ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif",
          "fontSize": 14,
          "fontWeight": 450,
          "lineHeight": 1.45,
          "textAlign": "left",
          "paddingX": 14,
          "paddingY": 10,
          "nodeMinWidth": 60,
          "nodeMinHeight": 40
        },
        "paint": {
          "bg": "#141218",
          "panel": "#1d1b20",
          "text": "#e6e1e5",
          "muted": "#cac4d0",
          "border": "rgba(202, 196, 208, 0.22)",
          "nodeFill": "#211f26",
          "nodeFillSelected": "#4f378b",
          "nodeStroke": "transparent",
          "nodeStrokeSelected": "#d0bcff",
          "edgeStroke": "#938f99",
          "relationStroke": "#efb8c8",
          "relationStrokeSelected": "#f2b8b5",
          "summaryStroke": "#49454f"
        }
      },
      "edges": {
        "strokeWidth": 4,
        "cap": "round",
        "join": "round",
        "routeType": "orthogonal-rounded"
      },
      "relations": {
        "strokeWidth": 2,
        "cap": "round",
        "join": "round"
      },
      "nodeShape": {
        "type": "rounded-rect",
        "radius": 16,
        "strokeWidth": 0
      },
      "rainbow": {
        "enabled": false,
        "palette": [
          "#ef4444",
          "#f97316",
          "#eab308",
          "#22c55e",
          "#06b6d4",
          "#3b82f6",
          "#8b5cf6",
          "#ec4899"
        ]
      },
      "background": {
        "color": "#141218"
      },
      "rules": {
        "nodeRules": [
          {
            "id": "m3-root",
            "priority": 10,
            "when": {
              "kind": "depth",
              "depth": 0
            },
            "apply": {
              "layout": {
                "textAlign": "center",
                "fontWeight": 700,
                "fontSize": 24,
                "paddingX": 18,
                "paddingY": 12
              },
              "paint": {
                "nodeFill": "#4f378b",
                "nodeFillSelected": "#6750a4",
                "text": "#fef7ff"
              },
              "incomingEdge": {
                "strokeColor": "#d0bcff",
                "strokeWidth": 2.5
              }
            }
          },
          {
            "id": "m3-depth-1",
            "priority": 10,
            "when": {
              "kind": "depth",
              "depth": 1
            },
            "apply": {
              "layout": {
                "fontWeight": 600,
                "fontSize": 18
              },
              "paint": {
                "nodeFill": "#332d41",
                "text": "#e6e1e5"
              },
              "incomingEdge": {
                "strokeColor": "#cbc2db",
                "routeType": "center-quadratic"
              }
            }
          },
          {
            "id": "m3-depth-2",
            "priority": 10,
            "when": {
              "kind": "depth",
              "depth": 2
            },
            "apply": {
              "paint": {
                "nodeFill": "#492532",
                "text": "#fef7ff"
              },
              "incomingEdge": {
                "strokeColor": "#efb8c8"
              }
            }
          },
          {
            "id": "m3-depth-3plus",
            "priority": 10,
            "when": {
              "kind": "depthRange",
              "minDepth": 3
            },
            "apply": {
              "incomingEdge": {
                "strokeWidth": 1.75
              }
            }
          }
        ]
      }
    }
  }
};

// ../themes/src/themes/material-3-slate.ts
var material3SlateTheme = {
  "schemaVersion": 1,
  "id": "kmind-material-3-slate",
  "name": "KMind Slate",
  "description": "Material 3 seed #303745",
  "variants": {
    "light": {
      "tokens": {
        "layout": {
          "fontFamily": "ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif",
          "fontSize": 14,
          "fontWeight": 450,
          "lineHeight": 1.45,
          "textAlign": "left",
          "paddingX": 14,
          "paddingY": 10,
          "nodeMinWidth": 60,
          "nodeMinHeight": 40
        },
        "paint": {
          "bg": "#f6f7fb",
          "panel": "#ffffff",
          "text": "#1a1f27",
          "muted": "#525b6b",
          "border": "#e1e6ef",
          "nodeFill": "#eef1f6",
          "nodeFillSelected": "#dfe5f0",
          "nodeStroke": "transparent",
          "nodeStrokeSelected": "#303745",
          "edgeStroke": "#606a7a",
          "relationStroke": "#4f5d78",
          "relationStrokeSelected": "#ba1a1a",
          "summaryStroke": "#c5cad4"
        }
      },
      "edges": {
        "strokeWidth": 4,
        "cap": "round",
        "join": "round",
        "routeType": "orthogonal-rounded"
      },
      "relations": {
        "strokeWidth": 2,
        "cap": "round",
        "join": "round"
      },
      "nodeShape": {
        "type": "rounded-rect",
        "radius": 16,
        "strokeWidth": 0
      },
      "rainbow": {
        "enabled": false,
        "palette": [
          "#303745",
          "#1b5fa7",
          "#0ea5e9",
          "#14b8a6",
          "#22c55e",
          "#f59e0b",
          "#fb7185",
          "#a78bfa"
        ]
      },
      "background": {
        "color": "#f6f7fb"
      },
      "rules": {
        "nodeRules": [
          {
            "id": "m3-root",
            "priority": 10,
            "when": {
              "kind": "depth",
              "depth": 0
            },
            "apply": {
              "layout": {
                "textAlign": "center",
                "fontWeight": 700,
                "fontSize": 24,
                "paddingX": 18,
                "paddingY": 12
              },
              "paint": {
                "nodeFill": "#3949a9",
                "nodeFillSelected": "#c9d3e5",
                "text": "#ffffff"
              }
            }
          },
          {
            "id": "m3-depth-1",
            "priority": 10,
            "when": {
              "kind": "depth",
              "depth": 1
            },
            "apply": {
              "layout": {
                "fontWeight": 600,
                "fontSize": 18
              },
              "paint": {
                "nodeFill": "#eef1f6",
                "text": "#1a1f27"
              },
              "incomingEdge": {
                "strokeColor": "#303745",
                "routeType": "center-quadratic"
              }
            }
          },
          {
            "id": "m3-depth-2",
            "priority": 10,
            "when": {
              "kind": "depth",
              "depth": 2
            },
            "apply": {
              "incomingEdge": {
                "strokeColor": "#4f5d78"
              }
            }
          },
          {
            "id": "m3-depth-3plus",
            "priority": 10,
            "when": {
              "kind": "depthRange",
              "minDepth": 3
            },
            "apply": {
              "incomingEdge": {
                "strokeWidth": 1.75
              }
            }
          }
        ]
      }
    },
    "dark": {
      "tokens": {
        "layout": {
          "fontFamily": "ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif",
          "fontSize": 14,
          "fontWeight": 450,
          "lineHeight": 1.45,
          "textAlign": "left",
          "paddingX": 14,
          "paddingY": 10,
          "nodeMinWidth": 60,
          "nodeMinHeight": 40
        },
        "paint": {
          "bg": "#0e1219",
          "panel": "#151a24",
          "text": "#e6e9ef",
          "muted": "#c5cad4",
          "border": "rgba(197, 202, 212, 0.22)",
          "nodeFill": "#1a202b",
          "nodeFillSelected": "#303745",
          "nodeStroke": "transparent",
          "nodeStrokeSelected": "#dfe5f0",
          "edgeStroke": "#a9b0bd",
          "relationStroke": "#8bb4ff",
          "relationStrokeSelected": "#ffb4ab",
          "summaryStroke": "#525b6b"
        }
      },
      "edges": {
        "strokeWidth": 4,
        "cap": "round",
        "join": "round",
        "routeType": "orthogonal-rounded"
      },
      "relations": {
        "strokeWidth": 2,
        "cap": "round",
        "join": "round"
      },
      "nodeShape": {
        "type": "rounded-rect",
        "radius": 16,
        "strokeWidth": 0
      },
      "rainbow": {
        "enabled": false,
        "palette": [
          "#303745",
          "#1b5fa7",
          "#0ea5e9",
          "#14b8a6",
          "#22c55e",
          "#f59e0b",
          "#fb7185",
          "#a78bfa"
        ]
      },
      "background": {
        "color": "#0e1219"
      },
      "rules": {
        "nodeRules": [
          {
            "id": "m3-root",
            "priority": 10,
            "when": {
              "kind": "depth",
              "depth": 0
            },
            "apply": {
              "layout": {
                "textAlign": "center",
                "fontWeight": 700,
                "fontSize": 24,
                "paddingX": 18,
                "paddingY": 12
              },
              "paint": {
                "nodeFill": "#303745",
                "nodeFillSelected": "#3a4354",
                "text": "#f6f7fb"
              }
            }
          },
          {
            "id": "m3-depth-1",
            "priority": 10,
            "when": {
              "kind": "depth",
              "depth": 1
            },
            "apply": {
              "layout": {
                "fontWeight": 600,
                "fontSize": 18
              },
              "paint": {
                "nodeFill": "#242b37",
                "text": "#e6e9ef"
              },
              "incomingEdge": {
                "strokeColor": "#c5cad4",
                "routeType": "center-quadratic"
              }
            }
          },
          {
            "id": "m3-depth-2",
            "priority": 10,
            "when": {
              "kind": "depth",
              "depth": 2
            },
            "apply": {
              "paint": {
                "nodeFill": "#1a2435",
                "text": "#dce3f3"
              },
              "incomingEdge": {
                "strokeColor": "#8bb4ff"
              }
            }
          },
          {
            "id": "m3-depth-3plus",
            "priority": 10,
            "when": {
              "kind": "depthRange",
              "minDepth": 3
            },
            "apply": {
              "incomingEdge": {
                "strokeWidth": 1.75
              }
            }
          }
        ]
      }
    }
  }
};

// ../themes/src/themes/midnight-neon.ts
var midnightNeonTheme = {
  "schemaVersion": 1,
  "id": "kmind-midnight-neon",
  "name": "Midnight Neon",
  "variants": {
    "light": {
      "tokens": {
        "layout": {
          "fontFamily": "ui-sans-serif, system-ui, sans-serif",
          "fontSize": 14,
          "fontWeight": 400,
          "lineHeight": 1.4,
          "textAlign": "left",
          "paddingX": 12,
          "paddingY": 8,
          "nodeMinWidth": 60,
          "nodeMinHeight": 34
        },
        "paint": {
          "bg": "#070a14",
          "panel": "#0b1020",
          "text": "#e2e8f0",
          "muted": "#94a3b8",
          "border": "rgba(148, 163, 184, 0.18)",
          "nodeFill": "#0b1020",
          "nodeFillSelected": "rgba(56, 189, 248, 0.14)",
          "nodeStroke": "#a855f7",
          "nodeStrokeSelected": "#22c55e",
          "edgeStroke": "#a855f7",
          "relationStroke": "#f59e0b",
          "relationStrokeSelected": "#fb7185",
          "summaryStroke": "rgba(168, 85, 247, 0.65)"
        }
      },
      "edges": {
        "routeType": "center-quadratic-tapered",
        "strokeWidth": 4,
        "cap": "round",
        "join": "round"
      },
      "relations": {
        "strokeWidth": 2,
        "cap": "round",
        "join": "round"
      },
      "nodeShape": {
        "type": "rounded-rect",
        "radius": 14,
        "strokeWidth": 3
      },
      "rainbow": {
        "enabled": true,
        "palette": [
          "#ef4444",
          "#f97316",
          "#eab308",
          "#22c55e",
          "#06b6d4",
          "#3b82f6",
          "#8b5cf6",
          "#ec4899"
        ]
      },
      "rules": {
        "nodeRules": [
          {
            "id": "root",
            "priority": 10,
            "when": {
              "kind": "depth",
              "depth": 0
            },
            "apply": {
              "layout": {
                "fontSize": 24,
                "textAlign": "center",
                "fontWeight": 800
              }
            }
          },
          {
            "id": "first",
            "priority": 10,
            "when": {
              "kind": "depth",
              "depth": 1
            },
            "apply": {
              "layout": {
                "fontSize": 18,
                "fontWeight": 600
              }
            }
          }
        ]
      }
    },
    "dark": {
      "tokens": {
        "layout": {
          "fontFamily": "ui-sans-serif, system-ui, sans-serif",
          "fontSize": 14,
          "fontWeight": 400,
          "lineHeight": 1.4,
          "textAlign": "left",
          "paddingX": 12,
          "paddingY": 8,
          "nodeMinWidth": 60,
          "nodeMinHeight": 34
        },
        "paint": {
          "bg": "#070a14",
          "panel": "#0b1020",
          "text": "#e2e8f0",
          "muted": "#94a3b8",
          "border": "rgba(148, 163, 184, 0.18)",
          "nodeFill": "#0b1020",
          "nodeFillSelected": "rgba(56, 189, 248, 0.14)",
          "nodeStroke": "#a855f7",
          "nodeStrokeSelected": "#22c55e",
          "edgeStroke": "#a855f7",
          "relationStroke": "#f59e0b",
          "relationStrokeSelected": "#fb7185",
          "summaryStroke": "rgba(168, 85, 247, 0.65)"
        }
      },
      "edges": {
        "routeType": "center-quadratic-tapered",
        "strokeWidth": 4,
        "cap": "round",
        "join": "round"
      },
      "relations": {
        "strokeWidth": 2,
        "cap": "round",
        "join": "round"
      },
      "nodeShape": {
        "type": "rounded-rect",
        "radius": 14,
        "strokeWidth": 3
      },
      "rainbow": {
        "enabled": true,
        "palette": [
          "#ef4444",
          "#f97316",
          "#eab308",
          "#22c55e",
          "#06b6d4",
          "#3b82f6",
          "#8b5cf6",
          "#ec4899"
        ]
      },
      "rules": {
        "nodeRules": [
          {
            "id": "root",
            "priority": 10,
            "when": {
              "kind": "depth",
              "depth": 0
            },
            "apply": {
              "layout": {
                "fontSize": 24,
                "textAlign": "center"
              }
            }
          },
          {
            "id": "first",
            "priority": 10,
            "when": {
              "kind": "depth",
              "depth": 1
            },
            "apply": {
              "layout": {
                "fontSize": 18
              }
            }
          }
        ]
      }
    }
  }
};

// ../themes/src/themes/rainbow-breeze.ts
var rainbowBreezeTheme = {
  "schemaVersion": 1,
  "id": "kmind-rainbow-breeze",
  "name": "Rainbow Breeze",
  "variants": {
    "light": {
      "tokens": {
        "layout": {
          "fontFamily": "ui-sans-serif, system-ui, sans-serif",
          "fontSize": 14,
          "fontWeight": 400,
          "lineHeight": 1.4,
          "textAlign": "left",
          "paddingX": 12,
          "paddingY": 8,
          "nodeMinWidth": 60,
          "nodeMinHeight": 34
        },
        "paint": {
          "bg": "#f8fafc",
          "panel": "#ffffff",
          "text": "#0f172a",
          "muted": "#64748b",
          "border": "#e2e8f0",
          "nodeFill": "#ffffff",
          "nodeFillSelected": "rgba(14, 165, 233, 0.08)",
          "nodeStroke": "#0ea5e9",
          "nodeStrokeSelected": "#a78bfa",
          "edgeStroke": "#0ea5e9",
          "relationStroke": "#fb7185",
          "relationStrokeSelected": "#a78bfa",
          "summaryStroke": "rgba(14, 165, 233, 0.45)"
        }
      },
      "edges": {
        "routeType": "edge-lead-quadratic",
        "strokeWidth": 3,
        "cap": "round",
        "join": "round"
      },
      "relations": {
        "strokeWidth": 2,
        "cap": "round",
        "join": "round"
      },
      "nodeShape": {
        "type": "rounded-rect",
        "radius": 16,
        "strokeWidth": 2.5
      },
      "rainbow": {
        "enabled": true,
        "palette": [
          "#fb7185",
          "#f97316",
          "#fbbf24",
          "#34d399",
          "#22d3ee",
          "#60a5fa",
          "#a78bfa",
          "#f472b6"
        ]
      },
      "rules": {
        "nodeRules": [
          {
            "id": "root",
            "priority": 10,
            "when": {
              "kind": "depth",
              "depth": 0
            },
            "apply": {
              "layout": {
                "fontSize": 24,
                "fontWeight": 800,
                "textAlign": "center"
              },
              "paint": {
                "text": "#ffffff",
                "nodeFill": "#e53935",
                "nodeStroke": "transparent"
              }
            }
          },
          {
            "id": "first",
            "priority": 10,
            "when": {
              "kind": "depth",
              "depth": 1
            },
            "apply": {
              "layout": {
                "fontSize": 18,
                "fontWeight": 700
              }
            }
          }
        ]
      }
    },
    "dark": {
      "tokens": {
        "layout": {
          "fontFamily": "ui-sans-serif, system-ui, sans-serif",
          "fontSize": 14,
          "fontWeight": 400,
          "lineHeight": 1.4,
          "textAlign": "left",
          "paddingX": 12,
          "paddingY": 8,
          "nodeMinWidth": 60,
          "nodeMinHeight": 34
        },
        "paint": {
          "bg": "#0b1020",
          "panel": "#0f172a",
          "text": "#e2e8f0",
          "muted": "#94a3b8",
          "border": "rgba(148, 163, 184, 0.18)",
          "nodeFill": "#0f172a",
          "nodeFillSelected": "rgba(56, 189, 248, 0.16)",
          "nodeStroke": "#38bdf8",
          "nodeStrokeSelected": "#a78bfa",
          "edgeStroke": "#38bdf8",
          "relationStroke": "#fb7185",
          "relationStrokeSelected": "#a78bfa",
          "summaryStroke": "rgba(56, 189, 248, 0.55)"
        }
      },
      "edges": {
        "routeType": "edge-lead-quadratic",
        "strokeWidth": 3,
        "cap": "round",
        "join": "round"
      },
      "relations": {
        "strokeWidth": 2,
        "cap": "round",
        "join": "round"
      },
      "nodeShape": {
        "type": "rounded-rect",
        "radius": 16,
        "strokeWidth": 2.5
      },
      "rainbow": {
        "enabled": true,
        "palette": [
          "#fb7185",
          "#f97316",
          "#fbbf24",
          "#34d399",
          "#22d3ee",
          "#60a5fa",
          "#a78bfa",
          "#f472b6"
        ]
      },
      "rules": {
        "nodeRules": [
          {
            "id": "root",
            "priority": 10,
            "when": {
              "kind": "depth",
              "depth": 0
            },
            "apply": {
              "layout": {
                "fontSize": 24,
                "fontWeight": 800,
                "textAlign": "center"
              },
              "paint": {
                "text": "#ffffff",
                "nodeFill": "#e53935",
                "nodeStroke": "transparent"
              }
            }
          },
          {
            "id": "first",
            "priority": 10,
            "when": {
              "kind": "depth",
              "depth": 1
            },
            "apply": {
              "layout": {
                "fontSize": 18,
                "fontWeight": 700
              }
            }
          }
        ]
      }
    }
  }
};

// ../themes/src/presets.ts
var DEFAULT_THEME_PRESET_ID = "kmind-material-3-slate";
var defaultTheme = createDefaultThemeDefinition();
var THEME_PRESETS = [
  { id: defaultTheme.id, name: defaultTheme.name, theme: defaultTheme },
  { id: material3SlateTheme.id, name: material3SlateTheme.name, theme: material3SlateTheme },
  { id: material3Theme.id, name: material3Theme.name, theme: material3Theme, visibility: { app: false } },
  { id: candyPopTheme.id, name: candyPopTheme.name, theme: candyPopTheme },
  { id: midnightNeonTheme.id, name: midnightNeonTheme.name, theme: midnightNeonTheme },
  { id: rainbowBreezeTheme.id, name: rainbowBreezeTheme.name, theme: rainbowBreezeTheme },
  { id: baselineForkInkTheme.id, name: baselineForkInkTheme.name, theme: baselineForkInkTheme, visibility: { app: false } },
  { id: material3RoundedOrthogonalVioletTheme.id, name: material3RoundedOrthogonalVioletTheme.name, theme: material3RoundedOrthogonalVioletTheme },
  { id: material3RoundedOrthogonalOceanTheme.id, name: material3RoundedOrthogonalOceanTheme.name, theme: material3RoundedOrthogonalOceanTheme },
  { id: material3RoundedOrthogonalForestTheme.id, name: material3RoundedOrthogonalForestTheme.name, theme: material3RoundedOrthogonalForestTheme },
  { id: material3RoundedOrthogonalCitrusTheme.id, name: material3RoundedOrthogonalCitrusTheme.name, theme: material3RoundedOrthogonalCitrusTheme },
  { id: material3RoundedOrthogonalRoseTheme.id, name: material3RoundedOrthogonalRoseTheme.name, theme: material3RoundedOrthogonalRoseTheme },
  { id: material3RoundedOrthogonalAquaTheme.id, name: material3RoundedOrthogonalAquaTheme.name, theme: material3RoundedOrthogonalAquaTheme }
];
var THEME_PRESETS_APP = THEME_PRESETS.filter((preset) => preset.visibility?.app !== false);
function resolveThemePreset(presetId) {
  const id = String(presetId ?? "").trim();
  if (!id) return null;
  return THEME_PRESETS.find((preset) => preset.id === id) ?? null;
}

// ../app/src/services/project-manifest-v1.ts
var PROJECT_MANIFEST_ASSET_ID = "kmind.project-manifest.v1";
function normalizeSubmapIds(raw) {
  if (!Array.isArray(raw)) return [];
  const seen = /* @__PURE__ */ new Set();
  const out = [];
  for (const item of raw) {
    const id = typeof item === "string" ? item.trim() : "";
    if (!id) continue;
    const docId = id;
    if (seen.has(docId)) continue;
    seen.add(docId);
    out.push(docId);
  }
  return out;
}
function getProjectManifestV1(doc) {
  const asset = doc.assets?.[PROJECT_MANIFEST_ASSET_ID];
  if (!asset || asset.kind !== "json") return null;
  const data = asset.data;
  if (!data || data.schemaVersion !== 1) return null;
  const submaps = normalizeSubmapIds(data.submaps);
  return { schemaVersion: 1, submaps };
}
function upsertProjectManifestV1(doc, manifest) {
  const existing = doc.assets?.[PROJECT_MANIFEST_ASSET_ID];
  const nextAsset = { id: PROJECT_MANIFEST_ASSET_ID, kind: "json", data: manifest };
  const nextAssets = { ...doc.assets ?? {} };
  if (!existing || existing.kind !== "json" || existing.data !== manifest) {
    nextAssets[PROJECT_MANIFEST_ASSET_ID] = nextAsset;
  }
  return { ...doc, assets: nextAssets };
}
function ensureProjectManifestV1(doc) {
  const existing = getProjectManifestV1(doc);
  if (existing) {
    const normalized = existing.submaps.length === 0 ? existing : { schemaVersion: 1, submaps: [...existing.submaps] };
    if (normalized.submaps.join("|") === existing.submaps.join("|")) return { doc, manifest: existing, changed: false };
    const nextDoc2 = upsertProjectManifestV1(doc, normalized);
    return { doc: nextDoc2, manifest: normalized, changed: nextDoc2 !== doc };
  }
  const created = { schemaVersion: 1, submaps: [] };
  const nextDoc = upsertProjectManifestV1(doc, created);
  return { doc: nextDoc, manifest: created, changed: nextDoc !== doc };
}

// ../app/src/services/project-settings-v1.ts
var PROJECT_SETTINGS_ASSET_ID = "kmind.project-settings.v1";
var ROOT_LAYOUT_SOURCE_KEY_V1 = "kmind.rootLayout.source.v1";
function getProjectSettingsV1(doc) {
  const asset = doc.assets?.[PROJECT_SETTINGS_ASSET_ID];
  if (!asset || asset.kind !== "json") return null;
  const data = asset.data;
  if (!data || data.schemaVersion !== 1) return null;
  if (typeof data.defaultRootLayout !== "string") return null;
  const backgroundColorRaw = data.backgroundColor;
  const backgroundColor = typeof backgroundColorRaw === "string" ? backgroundColorRaw.trim() : "";
  const settings = {
    schemaVersion: 1,
    defaultRootLayout: data.defaultRootLayout
  };
  const layoutOptions = normalizeProjectLayoutOptionsV1(data.layoutOptions);
  const rootLayoutOptions = normalizeProjectRootLayoutOptionsMapV1(data.rootLayoutOptions);
  const themeDefaults = normalizeProjectSettingsThemeDefaultsSourceV1(data.themeDefaults);
  if (backgroundColor.length > 0) {
    return {
      ...settings,
      backgroundColor,
      ...layoutOptions ? { layoutOptions } : {},
      ...rootLayoutOptions ? { rootLayoutOptions } : {},
      ...themeDefaults ? { themeDefaults } : {}
    };
  }
  return {
    ...settings,
    ...layoutOptions ? { layoutOptions } : {},
    ...rootLayoutOptions ? { rootLayoutOptions } : {},
    ...themeDefaults ? { themeDefaults } : {}
  };
}
function upsertProjectSettingsV1(doc, settings) {
  const existing = doc.assets?.[PROJECT_SETTINGS_ASSET_ID];
  const nextAsset = { id: PROJECT_SETTINGS_ASSET_ID, kind: "json", data: settings };
  const nextAssets = { ...doc.assets ?? {} };
  if (!existing || existing.kind !== "json" || existing.data !== settings) {
    nextAssets[PROJECT_SETTINGS_ASSET_ID] = nextAsset;
  }
  return { ...doc, assets: nextAssets };
}
function normalizeProjectLayoutOptionsV1(value) {
  if (!value || typeof value !== "object" || Array.isArray(value)) return void 0;
  const raw = value;
  let next = {};
  const horizontalGap = normalizeGap(raw.horizontalGap, 0, 400);
  const verticalGap = normalizeGap(raw.verticalGap, 0, 240);
  const rootGap = normalizeGap(raw.rootGap, 0, 400);
  if (horizontalGap !== void 0) next = { ...next, horizontalGap };
  if (verticalGap !== void 0) next = { ...next, verticalGap };
  if (rootGap !== void 0) next = { ...next, rootGap };
  const logicalAlign = raw.tidy?.logicalAlign === "level" || raw.tidy?.logicalAlign === "subtree" ? raw.tidy.logicalAlign : void 0;
  const packing = raw.tidy?.packing === "compact" || raw.tidy?.packing === "relaxed" ? raw.tidy.packing : void 0;
  if (logicalAlign || packing) {
    next = { ...next, tidy: { ...logicalAlign ? { logicalAlign } : {}, ...packing ? { packing } : {} } };
  }
  return Object.keys(next).length > 0 ? next : void 0;
}
function normalizeProjectRootLayoutOptionsV1(value) {
  if (!value || typeof value !== "object" || Array.isArray(value)) return void 0;
  const raw = value;
  let next = {};
  const horizontalGap = normalizeGap(raw.horizontalGap, 0, 400);
  const verticalGap = normalizeGap(raw.verticalGap, 0, 240);
  if (horizontalGap !== void 0) next = { ...next, horizontalGap };
  if (verticalGap !== void 0) next = { ...next, verticalGap };
  return Object.keys(next).length > 0 ? next : void 0;
}
function normalizeProjectRootLayoutOptionsMapV1(value) {
  if (!value || typeof value !== "object" || Array.isArray(value)) return void 0;
  const entries = [];
  for (const [rootId, rawOptions] of Object.entries(value)) {
    const normalizedRootId = rootId.trim();
    if (!normalizedRootId) continue;
    const rootOptions = normalizeProjectRootLayoutOptionsV1(rawOptions);
    if (!rootOptions) continue;
    entries.push([normalizedRootId, rootOptions]);
  }
  return entries.length > 0 ? Object.fromEntries(entries) : void 0;
}
function normalizeProjectSettingsThemeDefaultsSourceV1(value) {
  if (!value || typeof value !== "object" || Array.isArray(value)) return void 0;
  const raw = value;
  if (raw.schemaVersion !== 1) return void 0;
  const themePackageId = typeof raw.themePackageId === "string" ? raw.themePackageId.trim() : "";
  if (!themePackageId) return void 0;
  const fields = normalizeProjectSettingsThemeDefaultsFieldsV1(raw.fields);
  if (!fields) return void 0;
  return { schemaVersion: 1, themePackageId, fields };
}
function normalizeProjectSettingsThemeDefaultsFieldsV1(value) {
  if (!value || typeof value !== "object" || Array.isArray(value)) return void 0;
  const raw = value;
  let fields = {};
  if (raw.defaultRootLayout === true) fields = { ...fields, defaultRootLayout: true };
  if (raw.backgroundColor === true) fields = { ...fields, backgroundColor: true };
  const layoutOptions = normalizeProjectSettingsThemeDefaultsLayoutOptionsFieldsV1(raw.layoutOptions);
  if (layoutOptions) fields = { ...fields, layoutOptions };
  return hasProjectSettingsThemeDefaultsFields(fields) ? fields : void 0;
}
function hasProjectSettingsThemeDefaultsFields(fields) {
  if (!fields) return false;
  if (fields.defaultRootLayout || fields.backgroundColor) return true;
  return Boolean(normalizeProjectSettingsThemeDefaultsLayoutOptionsFieldsV1(fields.layoutOptions));
}
function normalizeProjectSettingsThemeDefaultsLayoutOptionsFieldsV1(value) {
  if (!value || typeof value !== "object" || Array.isArray(value)) return void 0;
  const raw = value;
  let fields = {};
  if (raw.horizontalGap === true) fields = { ...fields, horizontalGap: true };
  if (raw.verticalGap === true) fields = { ...fields, verticalGap: true };
  if (raw.rootGap === true) fields = { ...fields, rootGap: true };
  const tidyRaw = raw.tidy;
  if (tidyRaw && typeof tidyRaw === "object" && !Array.isArray(tidyRaw)) {
    const tidy = {
      ...tidyRaw.logicalAlign === true ? { logicalAlign: true } : {},
      ...tidyRaw.packing === true ? { packing: true } : {}
    };
    if (Object.keys(tidy).length > 0) fields = { ...fields, tidy };
  }
  return fields.horizontalGap || fields.verticalGap || fields.rootGap || fields.tidy ? fields : void 0;
}
function normalizeGap(value, min, max) {
  if (typeof value !== "number" || !Number.isFinite(value)) return void 0;
  return Math.max(min, Math.min(max, Math.round(value)));
}
function readRootLayoutSource(node) {
  const value = node.data?.[ROOT_LAYOUT_SOURCE_KEY_V1];
  if (value === "project-default" || value === "explicit") return value;
  return null;
}
function writeRootLayoutSource(node, source) {
  const nextData = { ...node.data ?? {} };
  nextData[ROOT_LAYOUT_SOURCE_KEY_V1] = source;
  return { ...node, data: nextData };
}
function isRootNode(doc, nodeId) {
  return doc.roots.includes(nodeId);
}
function applyProjectDefaultRootLayoutV1(args) {
  const rootIds = args.doc.roots.filter((id) => Boolean(args.doc.nodes[id]));
  if (rootIds.length === 0) return { doc: args.doc, changed: false };
  let changed = false;
  const nextNodes = { ...args.doc.nodes };
  for (const rootId of rootIds) {
    const node = nextNodes[rootId];
    if (!node) continue;
    if (!isRootNode(args.doc, rootId)) continue;
    const source = readRootLayoutSource(node);
    if (!source) {
      if (node.layout) {
        nextNodes[rootId] = writeRootLayoutSource(node, "explicit");
        changed = true;
      } else {
        let nextNode = node;
        nextNode = writeRootLayoutSource(nextNode, "project-default");
        nextNode = { ...nextNode, layout: args.defaultRootLayout };
        nextNodes[rootId] = nextNode;
        changed = true;
      }
      continue;
    }
    if (source === "project-default") {
      if (node.layout !== args.defaultRootLayout) {
        nextNodes[rootId] = { ...node, layout: args.defaultRootLayout };
        changed = true;
      }
    }
  }
  if (!changed) return { doc: args.doc, changed: false };
  return { doc: { ...args.doc, nodes: nextNodes }, changed: true };
}

// ../app/src/utils/externalize-document-assets.ts
init_src();

// ../app/src/utils/bytes.ts
function concatBytes(chunks) {
  let total = 0;
  for (const chunk of chunks) total += chunk.byteLength;
  const out = new Uint8Array(total);
  let offset = 0;
  for (const chunk of chunks) {
    out.set(chunk, offset);
    offset += chunk.byteLength;
  }
  return out;
}
function encodeUtf8(text) {
  const Encoder = globalThis.TextEncoder;
  if (Encoder) return new Encoder().encode(text);
  const BufferCtor = globalThis.Buffer;
  if (BufferCtor) return BufferCtor.from(text, "utf-8");
  throw new Error("UTF-8 encoder is not available in the current environment.");
}
function decodeUtf8(bytes) {
  const Decoder = globalThis.TextDecoder;
  if (Decoder) return new Decoder("utf-8").decode(bytes);
  const BufferCtor = globalThis.Buffer;
  if (BufferCtor) return BufferCtor.from(bytes).toString("utf-8");
  throw new Error("UTF-8 decoder is not available in the current environment.");
}

// ../app/src/features/mindmap-feature.ts
init_src();

// ../app/src/utils/base64.ts
function encodeBase64(bytes) {
  const BufferCtor = globalThis.Buffer;
  if (BufferCtor) return BufferCtor.from(bytes).toString("base64");
  const btoaFn = globalThis.btoa;
  if (!btoaFn) throw new Error("Base64 encoder is not available in the current environment.");
  let binary = "";
  for (const byte of bytes) binary += String.fromCharCode(byte);
  return btoaFn(binary);
}
function decodeBase64(base64) {
  const atobFn = globalThis.atob;
  if (typeof atobFn === "function") {
    const bin = atobFn(base64);
    const bytes = new Uint8Array(bin.length);
    for (let i = 0; i < bin.length; i += 1) bytes[i] = bin.charCodeAt(i);
    return bytes;
  }
  const BufferCtor = globalThis.Buffer;
  if (BufferCtor) return BufferCtor.from(base64, "base64");
  throw new Error("Base64 decoder is not available in the current environment.");
}

// ../app/src/services/document-zip-v1.ts
init_dist();
init_src();

// ../app/src/utils/crc32.ts
var CRC32_TABLE = (() => {
  const table = new Uint32Array(256);
  for (let i = 0; i < 256; i += 1) {
    let c = i;
    for (let k = 0; k < 8; k += 1) {
      c = c & 1 ? 3988292384 ^ c >>> 1 : c >>> 1;
    }
    table[i] = c >>> 0;
  }
  return table;
})();
function crc32(bytes) {
  let crc = 4294967295;
  for (let i = 0; i < bytes.length; i += 1) {
    const byte = bytes[i] ?? 0;
    const idx = (crc ^ byte) & 255;
    const value = CRC32_TABLE[idx] ?? 0;
    crc = value ^ crc >>> 8;
  }
  return (crc ^ 4294967295) >>> 0;
}

// ../app/src/utils/zip.ts
function writeU16LE(view, offset, value) {
  view.setUint16(offset, value & 65535, true);
}
function writeU32LE(view, offset, value) {
  view.setUint32(offset, value >>> 0, true);
}
function readU16LE(view, offset) {
  return view.getUint16(offset, true);
}
function readU32LE(view, offset) {
  return view.getUint32(offset, true);
}
function findEndOfCentralDirectory(bytes) {
  const signature = 101010256;
  const maxScan = Math.max(0, bytes.length - 22 - 65535);
  const view = new DataView(bytes.buffer, bytes.byteOffset, bytes.byteLength);
  for (let i = bytes.length - 22; i >= maxScan; i -= 1) {
    if (readU32LE(view, i) !== signature) continue;
    return i;
  }
  return -1;
}
function createZipStore(files) {
  const sorted = files.slice().sort((a, b) => a.path.localeCompare(b.path));
  const localChunks = [];
  const centralChunks = [];
  let offset = 0;
  for (const file of sorted) {
    const nameBytes = encodeUtf8(file.path);
    const data = file.bytes;
    const crc = crc32(data);
    const localHeader = new Uint8Array(30 + nameBytes.length);
    const localView = new DataView(localHeader.buffer);
    writeU32LE(localView, 0, 67324752);
    writeU16LE(localView, 4, 20);
    writeU16LE(localView, 6, 0);
    writeU16LE(localView, 8, 0);
    writeU16LE(localView, 10, 0);
    writeU16LE(localView, 12, 0);
    writeU32LE(localView, 14, crc);
    writeU32LE(localView, 18, data.length);
    writeU32LE(localView, 22, data.length);
    writeU16LE(localView, 26, nameBytes.length);
    writeU16LE(localView, 28, 0);
    localHeader.set(nameBytes, 30);
    localChunks.push(localHeader, data);
    const central = new Uint8Array(46 + nameBytes.length);
    const centralView = new DataView(central.buffer);
    writeU32LE(centralView, 0, 33639248);
    writeU16LE(centralView, 4, 20);
    writeU16LE(centralView, 6, 20);
    writeU16LE(centralView, 8, 0);
    writeU16LE(centralView, 10, 0);
    writeU16LE(centralView, 12, 0);
    writeU16LE(centralView, 14, 0);
    writeU32LE(centralView, 16, crc);
    writeU32LE(centralView, 20, data.length);
    writeU32LE(centralView, 24, data.length);
    writeU16LE(centralView, 28, nameBytes.length);
    writeU16LE(centralView, 30, 0);
    writeU16LE(centralView, 32, 0);
    writeU16LE(centralView, 34, 0);
    writeU16LE(centralView, 36, 0);
    writeU32LE(centralView, 38, 0);
    writeU32LE(centralView, 42, offset);
    central.set(nameBytes, 46);
    centralChunks.push(central);
    offset += localHeader.length + data.length;
  }
  const centralDirectoryOffset = offset;
  const centralDirectory = concatBytes(centralChunks);
  offset += centralDirectory.length;
  const end = new Uint8Array(22);
  const endView = new DataView(end.buffer);
  writeU32LE(endView, 0, 101010256);
  writeU16LE(endView, 4, 0);
  writeU16LE(endView, 6, 0);
  writeU16LE(endView, 8, sorted.length);
  writeU16LE(endView, 10, sorted.length);
  writeU32LE(endView, 12, centralDirectory.length);
  writeU32LE(endView, 16, centralDirectoryOffset);
  writeU16LE(endView, 20, 0);
  return concatBytes([...localChunks, centralDirectory, end]);
}
function readZipStore(bytes, options) {
  const copy = options?.copy !== false;
  const eocdOffset = findEndOfCentralDirectory(bytes);
  if (eocdOffset < 0) throw new Error("Invalid zip: EOCD not found.");
  const view = new DataView(bytes.buffer, bytes.byteOffset, bytes.byteLength);
  const entryCount = readU16LE(view, eocdOffset + 10);
  const centralSize = readU32LE(view, eocdOffset + 12);
  const centralOffset = readU32LE(view, eocdOffset + 16);
  const centralEnd = centralOffset + centralSize;
  if (centralEnd > bytes.length) throw new Error("Invalid zip: central directory out of bounds.");
  const entries = [];
  let cursor = centralOffset;
  for (let i = 0; i < entryCount; i += 1) {
    if (readU32LE(view, cursor) !== 33639248) throw new Error("Invalid zip: central directory signature mismatch.");
    const compressionMethod = readU16LE(view, cursor + 10);
    const crc = readU32LE(view, cursor + 16);
    const compressedSize = readU32LE(view, cursor + 20);
    const uncompressedSize = readU32LE(view, cursor + 24);
    const nameLength = readU16LE(view, cursor + 28);
    const extraLength = readU16LE(view, cursor + 30);
    const commentLength = readU16LE(view, cursor + 32);
    const localHeaderOffset = readU32LE(view, cursor + 42);
    const nameStart = cursor + 46;
    const nameEnd = nameStart + nameLength;
    const nameBytes = copy ? bytes.slice(nameStart, nameEnd) : bytes.subarray(nameStart, nameEnd);
    const path6 = decodeUtf8(nameBytes);
    entries.push({ path: path6, compressionMethod, compressedSize, uncompressedSize, crc32: crc, localHeaderOffset });
    cursor = nameEnd + extraLength + commentLength;
  }
  const result2 = /* @__PURE__ */ new Map();
  for (const entry of entries) {
    if (entry.compressionMethod !== 0) {
      throw new Error(`Unsupported zip compression method: ${entry.compressionMethod} (${entry.path})`);
    }
    const localOffset = entry.localHeaderOffset;
    if (readU32LE(view, localOffset) !== 67324752) throw new Error("Invalid zip: local file header signature mismatch.");
    const nameLength = readU16LE(view, localOffset + 26);
    const extraLength = readU16LE(view, localOffset + 28);
    const dataStart = localOffset + 30 + nameLength + extraLength;
    const dataEnd = dataStart + entry.uncompressedSize;
    if (dataEnd > bytes.length) throw new Error("Invalid zip: entry data out of bounds.");
    const fileBytes = copy ? bytes.slice(dataStart, dataEnd) : bytes.subarray(dataStart, dataEnd);
    if (crc32(fileBytes) !== entry.crc32) throw new Error(`Invalid zip: CRC mismatch (${entry.path})`);
    result2.set(entry.path, fileBytes);
  }
  return result2;
}

// ../app/src/utils/image-package-v1.ts
var PNG_SIGNATURE = new Uint8Array([137, 80, 78, 71, 13, 10, 26, 10]);

// ../app/src/services/kmindz-file.ts
var METADATA_ID = "kmindz";
var KMINDZ_COLLAB_METADATA_ID = "kmindz-collab";
var KMINDZ_DOCS_METADATA_ID = "kmindz-docs";
var KMINDZ_ASSETS_METADATA_ID = "kmindz-assets";
function escapeXmlText(value) {
  return value.replaceAll("&", "&amp;").replaceAll("<", "&lt;").replaceAll(">", "&gt;");
}
function unescapeXmlText(value) {
  return value.replaceAll("&lt;", "<").replaceAll("&gt;", ">").replaceAll("&amp;", "&");
}
function extractMetadataContentById(svgText, id) {
  const source = String(svgText ?? "");
  const match = new RegExp(`<metadata\\b[^>]*\\bid=["']${id}["'][^>]*>([\\s\\S]*?)<\\/metadata>`, "i").exec(source);
  return match ? match[1] ?? null : null;
}
function normalizeEmbeddedText(value) {
  const trimmed = String(value ?? "").trim();
  if (!trimmed) return "";
  if (!/\s/.test(trimmed)) return trimmed;
  return trimmed.replace(/\s+/g, "");
}
function isValidProjectHeaderV3(value) {
  if (!value || typeof value !== "object") return false;
  const record = value;
  if (record.format !== "kmindz-project-svg" || record.version !== 3) return false;
  if (typeof record.rootDocId !== "string" || record.rootDocId.trim().length === 0) return false;
  if (typeof record.rev !== "string" || record.rev.trim().length === 0) return false;
  if (!record.documentsMeta || typeof record.documentsMeta !== "object") return false;
  const docs = record.documentsMeta;
  if (!docs[record.rootDocId]) return false;
  return true;
}
function parseKmindzProjectV3FromSvgText(svgText) {
  try {
    const headerRawContent = extractMetadataContentById(svgText, METADATA_ID);
    if (!headerRawContent) return null;
    const headerRaw = unescapeXmlText(String(headerRawContent).trim());
    if (!headerRaw) return null;
    const headerParsed = JSON.parse(headerRaw);
    if (!isValidProjectHeaderV3(headerParsed)) return null;
    const header = headerParsed;
    const collabUpdateB64 = normalizeEmbeddedText(extractMetadataContentById(svgText, KMINDZ_COLLAB_METADATA_ID)) || null;
    const docsZipB64 = normalizeEmbeddedText(extractMetadataContentById(svgText, KMINDZ_DOCS_METADATA_ID)) || null;
    const assetsZipB64 = normalizeEmbeddedText(extractMetadataContentById(svgText, KMINDZ_ASSETS_METADATA_ID)) || null;
    return { header, collabUpdateB64, docsZipB64, assetsZipB64 };
  } catch {
    return null;
  }
}
function stripMetadataBlocks(svgText, ids) {
  let next = String(svgText ?? "").trim();
  for (const id of ids) {
    next = next.replace(new RegExp(`<metadata\\b[^>]*\\bid=(['"])${id}\\1[^>]*>[\\s\\S]*?<\\/metadata>`, "ig"), "");
  }
  return next;
}
function encodeKmindzProjectV3IntoSvgText(args) {
  const preview = stripMetadataBlocks(String(args.previewSvg ?? ""), [
    METADATA_ID,
    KMINDZ_COLLAB_METADATA_ID,
    KMINDZ_DOCS_METADATA_ID,
    KMINDZ_ASSETS_METADATA_ID
  ]);
  const metadataBlocks = [];
  metadataBlocks.push(`<metadata id="${METADATA_ID}" data-kmind="kmindz-project-svg@v3">${escapeXmlText(JSON.stringify(args.header))}</metadata>`);
  const collab = String(args.collabUpdateB64 ?? "").trim();
  if (collab) {
    metadataBlocks.push(
      `<metadata id="${KMINDZ_COLLAB_METADATA_ID}" data-kmind="yjs-update@v1" data-encoding="base64">${collab}</metadata>`
    );
  }
  const docsZip = String(args.docsZipB64 ?? "").trim();
  if (docsZip) {
    metadataBlocks.push(
      `<metadata id="${KMINDZ_DOCS_METADATA_ID}" data-kmind="docs-zip@v1" data-encoding="base64" data-mime="application/zip">${docsZip}</metadata>`
    );
  }
  const assetsZip = String(args.assetsZipB64 ?? "").trim();
  if (assetsZip) {
    metadataBlocks.push(
      `<metadata id="${KMINDZ_ASSETS_METADATA_ID}" data-kmind="assets-zip@v1" data-encoding="base64" data-mime="application/zip">${assetsZip}</metadata>`
    );
  }
  const metadata = `
${metadataBlocks.join("\n")}
`;
  const svgStart = preview.indexOf("<svg");
  if (svgStart < 0) {
    return `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1 1" width="1" height="1">${metadata}</svg>`;
  }
  const openTagEnd = preview.indexOf(">", svgStart);
  if (openTagEnd < 0) return preview;
  return `${preview.slice(0, openTagEnd + 1)}${metadata}${preview.slice(openTagEnd + 1)}`;
}

// ../app/src/features/submap-feature.ts
init_src();

// ../app/src/features/node-content-feature.ts
init_src();

// ../icons/src/builtin-icons-generated.ts
var BUILTIN_ICONS = [
  {
    id: "kmind-icon://builtin/basic/bolt",
    group: "basic",
    name: "bolt",
    label: "Bolt",
    catalog: { "groupId": "basic", "groupLabel": "Basic", "order": 100, "surfaces": ["node-content", "external-link"] },
    viewBox: "0 0 24 24",
    aliases: ["kmind-icon://basic/bolt"],
    svg: `<svg viewBox="0 0 24 24" aria-hidden="true" focusable="false" width="100%" height="100%"><path d="M13 2L4 14h7l-1 8 10-14h-7l0-6z" fill="none" stroke="currentColor" stroke-width="2" stroke-linejoin="round"/></svg>`
  },
  {
    id: "kmind-icon://builtin/basic/flag",
    group: "basic",
    name: "flag",
    label: "Flag",
    catalog: { "groupId": "basic", "groupLabel": "Basic", "order": 100, "surfaces": ["node-content", "external-link"] },
    viewBox: "0 0 24 24",
    aliases: ["kmind-icon://basic/flag"],
    svg: `<svg viewBox="0 0 24 24" aria-hidden="true" focusable="false" width="100%" height="100%"><path d="M5 3v18" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"/><path d="M5 4h12l-2 4 2 4H5" fill="none" stroke="currentColor" stroke-width="2" stroke-linejoin="round"/></svg>`
  },
  {
    id: "kmind-icon://builtin/basic/folder",
    group: "basic",
    name: "folder",
    label: "Folder",
    catalog: { "groupId": "basic", "groupLabel": "Basic", "order": 100, "surfaces": ["node-content", "external-link"] },
    viewBox: "0 0 24 24",
    aliases: ["kmind-icon://basic/folder"],
    svg: `<svg viewBox="0 0 24 24" aria-hidden="true" focusable="false" width="100%" height="100%"><path d="M3 6.5h6l2 2H21v9A2.5 2.5 0 0 1 18.5 20h-13A2.5 2.5 0 0 1 3 17.5v-11z" fill="none" stroke="currentColor" stroke-width="2" stroke-linejoin="round"/></svg>`
  },
  {
    id: "kmind-icon://builtin/basic/star",
    group: "basic",
    name: "star",
    label: "Star",
    catalog: { "groupId": "basic", "groupLabel": "Basic", "order": 100, "surfaces": ["node-content", "external-link"] },
    viewBox: "0 0 24 24",
    aliases: ["kmind-icon://basic/star"],
    svg: `<svg viewBox="0 0 24 24" aria-hidden="true" focusable="false" width="100%" height="100%"><path d="M12 2l3.1 6.8L22 9.9l-5 4.9L18.2 22 12 18.6 5.8 22 7 14.8 2 9.9l6.9-1.1L12 2z" fill="none" stroke="currentColor" stroke-width="2" stroke-linejoin="round"/></svg>`
  },
  {
    id: "kmind-icon://builtin/brand/baidu",
    group: "brand",
    name: "baidu",
    label: "Baidu",
    catalog: { "groupId": "brand", "groupLabel": "Brand", "order": 200, "surfaces": ["node-content", "external-link"] },
    viewBox: "0 0 24 24",
    svg: `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="100%" height="100%" aria-hidden="true" focusable="false"><path fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M20.839 10.38h-8.656v3.33h5.065c-.092.81-.645 2.07-1.842 2.88c-.737.54-1.842.9-3.223.9c-3.079 0-5.525-2.572-5.525-5.58c0-2.923 2.585-5.49 5.525-5.49c1.75 0 2.855.72 3.591 1.35l2.579-2.52C16.787 3.9 14.669 3 12.183 3C8.592 3 5.461 4.98 3.987 7.95a8.8 8.8 0 0 0 0 8.1C5.461 19.02 8.592 21 12.183 21c2.486 0 4.604-.81 6.078-2.16c2.4-2.1 3.095-5.427 2.578-8.46"/></svg>`
  },
  {
    id: "kmind-icon://builtin/brand/siyuan",
    group: "brand",
    name: "siyuan",
    label: "SiYuan",
    catalog: { "groupId": "brand", "groupLabel": "Brand", "order": 200, "surfaces": ["node-content", "external-link"] },
    viewBox: "0 0 24 24",
    svg: `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="100%" height="100%" aria-hidden="true" focusable="false"><g transform="scale(0.0234375)"><path fill="#d23f31" d="M37.052 371.676l269.857-269.857v550.507l-269.857 269.857z"/><path fill="#3b3e43" d="M306.909 101.818l205.091 205.091v550.507l-205.091-205.091z"/><path fill="#d23f31" d="M512 306.909l205.091-205.091v550.507l-205.091 205.091z"/><path fill="#3b3e43" d="M717.091 101.818l269.857 269.857v550.507l-269.857-269.857z"/></g></svg>`
  },
  {
    id: "kmind-icon://builtin/business/bar-chart",
    group: "business",
    name: "bar-chart",
    label: "Metrics",
    catalog: { "groupId": "business", "groupLabel": "Business", "order": 150, "surfaces": ["node-content"] },
    viewBox: "0 0 32 32",
    svg: `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32" width="100%" height="100%" aria-hidden="true" focusable="false"><g fill="none"><path fill="#E1D8EC" d="M2 6a4 4 0 0 1 4-4h20a4 4 0 0 1 4 4v20c0 1.48-.804 2.773-2 3.465L26.554 29a4 4 0 0 0-3.014.23L22 30h-3l-3-1.5l-3 1.5h-3l-1.54-.77A4 4 0 0 0 5.446 29L4 29.465A4 4 0 0 1 2 26z"/><path fill="#B4ACBC" d="M10 11v10H2v1h8v8h1v-8h10v8h1v-8h8v-1h-8V11h8v-1h-8V2h-1v8H11V2h-1v8H2v1zm1 0h10v10H11z"/><path fill="#00D26A" d="M6 30h4V10.214C10 9.542 9.453 9 8.774 9H5.226C4.547 9 4 9.542 4 10.213v19.252c.588.34 1.271.535 2 .535"/><path fill="#F70A8D" d="M17.774 17h-3.548c-.679 0-1.226.542-1.226 1.214V30h6V18.214c0-.672-.547-1.214-1.226-1.214"/><path fill="#00A6ED" d="M22 30h4c.729 0 1.412-.195 2-.535V7.209C28 6.539 27.453 6 26.774 6h-3.548C22.547 6 22 6.54 22 7.209z"/></g></svg>`
  },
  {
    id: "kmind-icon://builtin/business/briefcase",
    group: "business",
    name: "briefcase",
    label: "Work",
    catalog: { "groupId": "business", "groupLabel": "Business", "order": 150, "surfaces": ["node-content"] },
    viewBox: "0 0 32 32",
    svg: `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32" width="100%" height="100%" aria-hidden="true" focusable="false"><g fill="none"><path fill="#8C5543" d="M2 15h28v13a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2z"/><path fill="#6D4534" d="M11.1 9H4a2 2 0 0 0-2 2v4a4 4 0 0 0 4 4h20a4 4 0 0 0 4-4v-4a2 2 0 0 0-2-2h-7.1a5.002 5.002 0 0 0-9.8 0m2.07 0a3.001 3.001 0 0 1 5.66 0z"/><path fill="#D3883E" d="m13 19l3-1l3 1v2a1 1 0 0 1-1 1h-4a1 1 0 0 1-1-1z"/><path fill="#E19747" d="M13 18a1 1 0 0 1 1-1h4a1 1 0 0 1 1 1v1h-6z"/></g></svg>`
  },
  {
    id: "kmind-icon://builtin/business/chart-increasing",
    group: "business",
    name: "chart-increasing",
    label: "Growth",
    catalog: { "groupId": "business", "groupLabel": "Business", "order": 150, "surfaces": ["node-content"] },
    viewBox: "0 0 32 32",
    svg: `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32" width="100%" height="100%" aria-hidden="true" focusable="false"><g fill="none"><path fill="#E1D8EC" d="M2 6a4 4 0 0 1 4-4h20a4 4 0 0 1 3.731 2.556l-.585 1.776l.854.846V26a4 4 0 0 1-4 4H6a4 4 0 0 1-3.888-3.056l.67-1.893l-.782-.71z"/><path fill="#B4ACBC" d="M10 11v10H2v1h8v8h1v-8h10v8h1v-8h8v-1h-8V11h8v-1h-8V2h-1v8H11V2h-1v8H2v1zm1 0h10v10H11z"/><path fill="#319FE7" d="M2.12 26.976A4 4 0 0 1 2 26v-1.701l7.062-6.973a2.2 2.2 0 0 1 3.06-.03l2.15 2.04a.5.5 0 0 0 .698-.009L29.722 4.531c.18.455.278.95.278 1.469v1.187L16.132 20.902a2.2 2.2 0 0 1-3.052.04l-2.15-2.017a.5.5 0 0 0-.694.01z"/></g></svg>`
  },
  {
    id: "kmind-icon://builtin/business/dollar-banknote",
    group: "business",
    name: "dollar-banknote",
    label: "Budget",
    catalog: { "groupId": "business", "groupLabel": "Business", "order": 150, "surfaces": ["node-content"] },
    viewBox: "0 0 32 32",
    svg: `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32" width="100%" height="100%" aria-hidden="true" focusable="false"><g fill="none"><path fill="#00F397" d="M2 10a2 2 0 0 1 2-2h11l2 1l2-1h9a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2z"/><path fill="#008463" d="M3 11a2 2 0 0 1 2-2h22a2 2 0 0 1 2 2v12a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2zm2-1a1 1 0 0 0-1 1v12a1 1 0 0 0 1 1h22a1 1 0 0 0 1-1V11a1 1 0 0 0-1-1zM2 28a2 2 0 0 0 2 2h11l2-1l2 1h9a2 2 0 0 0 2-2v-4a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2zm24-11a4.5 4.5 0 1 1-9 0a4.5 4.5 0 0 1 9 0"/><path fill="#FFF478" d="M19 8h-4v19h4z"/><path fill="#F3AD61" d="M19 26h-4v4h4z"/><path fill="#fff" d="M9.5 12a.5.5 0 0 1 .5.5v.545c.834.152 1.517.678 1.824 1.375c.13.294-.122.58-.443.58c-.244 0-.448-.173-.587-.373C10.55 14.273 10.1 14 9.5 14c-.93 0-1.5.656-1.5 1.25s.57 1.25 1.5 1.25c1.38 0 2.5 1.007 2.5 2.25c0 1.088-.859 1.997-2 2.205v.545a.5.5 0 0 1-1 0v-.545c-.834-.152-1.517-.678-1.824-1.375c-.13-.294.122-.58.443-.58c.244 0 .448.173.587.373c.243.354.694.627 1.294.627c.93 0 1.5-.656 1.5-1.25s-.57-1.25-1.5-1.25c-1.38 0-2.5-1.007-2.5-2.25c0-1.088.859-1.996 2-2.205V12.5a.5.5 0 0 1 .5-.5"/></g></svg>`
  },
  {
    id: "kmind-icon://builtin/business/globe-with-meridians",
    group: "business",
    name: "globe-with-meridians",
    label: "Global",
    catalog: { "groupId": "business", "groupLabel": "Business", "order": 150, "surfaces": ["node-content"] },
    viewBox: "0 0 32 32",
    svg: `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32" width="100%" height="100%" aria-hidden="true" focusable="false"><path fill="#83CBFF" d="M2 16C2 8.28 8.28 2 16 2s14 6.28 14 14s-6.28 14-14 14S2 23.72 2 16m2.041-1h3.99a16 16 0 0 1 1.129-5H5.609a11.9 11.9 0 0 0-1.568 5m5.994 0H15v-5h-3.654a14 14 0 0 0-1.31 5M15 17h-4.965a14 14 0 0 0 1.31 5H15zm0 7h-2.494A14 14 0 0 0 15 26.73zm4.005 3.62A12 12 0 0 0 24.94 24h-3.074a16 16 0 0 1-2.86 3.62M22.84 22h3.55v.002A11.9 11.9 0 0 0 27.959 17h-3.99a16 16 0 0 1-1.13 5m-.875-5H17v5h3.654a14 14 0 0 0 1.31-5m2.004-2h3.99a11.9 11.9 0 0 0-1.569-5.002V10h-3.55a16 16 0 0 1 1.13 5m-3.315-5H17v5h4.965a14 14 0 0 0-1.31-5m1.212-2h3.073a12 12 0 0 0-5.926-3.618A16 16 0 0 1 21.865 8M17 5.27V8h2.494A14 14 0 0 0 17 5.27m-2 0A14 14 0 0 0 12.506 8H15zM17 24v2.73A14 14 0 0 0 19.494 24zM5.609 22h3.554a16 16 0 0 1-1.132-5H4.04c.15 1.81.703 3.506 1.568 5M13 27.621A16 16 0 0 1 10.14 24H7.06a12 12 0 0 0 5.941 3.621M10.134 8a16 16 0 0 1 2.853-3.617A12 12 0 0 0 7.061 8z"/></svg>`
  },
  {
    id: "kmind-icon://builtin/business/laptop",
    group: "business",
    name: "laptop",
    label: "Computer",
    catalog: { "groupId": "business", "groupLabel": "Business", "order": 150, "surfaces": ["node-content"] },
    viewBox: "0 0 32 32",
    svg: `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32" width="100%" height="100%" aria-hidden="true" focusable="false"><g fill="none"><path fill="#D3D3D3" d="m28 20l-12-1l-12 1l-1.98 8.891c-.11.766.975.609 1.48.609h25c.505 0 1.59.157 1.48-.609z"/><path fill="#7167A4" d="M27 2H5c-.55 0-1 .45-1 1v16.99h24V3c0-.55-.45-1-1-1"/><path fill="#26C9FC" d="M5 18.74V3.25c0-.14.11-.25.25-.25h21.5c.14 0 .25.11.25.25v15.49c0 .14-.11.25-.25.25H5.25c-.14 0-.25-.11-.25-.25"/><path fill="#9B9B9B" fill-rule="evenodd" d="m27.27 21.28l.72 3.25a.38.38 0 0 1-.37.46H4.38c-.24 0-.42-.23-.37-.46l.72-3.25c.04-.17.19-.29.37-.29h21.8c.18 0 .33.12.37.29M8.186 24.5H6.753l.125-.75H8.28zm1.938 0H8.69l.094-.75h1.404zm1.838 0h-1.336l.062-.75h1.306zm1.85 0h-1.35l.032-.75h1.35zm1.938 0h-1.437l.031-.75h1.406zm1.937 0H16.25v-.75h1.406zm1.85 0h-1.35l-.03-.75h1.349zm1.837 0h-1.336l-.032-.75h1.306zm1.937 0h-1.435l-.063-.75h1.404zm1.936 0h-1.433l-.093-.75h1.4zm1.753 0h-1.247l-.125-.75h1.247zm-.333-2l.125.75h-1.247l-.125-.75zm-.167-1l.083.5h-1.246l-.084-.5zm-3.06 0h1.307l.083.5h-1.328zm-1.814 0h1.31l.062.5h-1.33zm-1.713 0h1.211l.042.5h-1.233zm-1.85 0h1.35l.02.5h-1.35zm-1.813 0h1.312l.021.5H16.25zm-1.812 0h1.312v.5h-1.333zm-1.85 0h1.35l-.022.5h-1.35zm-1.712 0h1.211l-.02.5h-1.233zm-1.812 0h1.31l-.042.5h-1.33zm-1.81 0H8.56l-.063.5H7.17zm-1.754 0h1.247l-.084.5H5.417zm-.292 1.75l.125-.75H6.58l-.125.75zM5 24.5l.125-.75h1.247l-.125.75zm20.038-1.25l-.125-.75h-1.349l.094.75zm-1.884 0l-.093-.75h-1.352l.063.75zm-1.884 0l-.062-.75h-1.254l.032.75zm-1.785 0l-.031-.75h-1.35l.032.75zm-1.85 0l-.031-.75H16.25v.75zM7.087 22.5l-.125.75h1.38l.094-.75zm1.852 0l-.093.75h1.382l.063-.75zm1.854 0l-.063.75h1.284l.032-.75zm1.753 0l-.031.75h1.35l.03-.75zm1.85 0l-.031.75h1.385v-.75z" clip-rule="evenodd"/><path fill="#9B9B9B" d="M29.09 29a.9.9 0 0 0 .8-.49l.09.38l.003.023A.913.913 0 0 1 29.09 30H2.91c-.5 0-.91-.41-.91-.91c0-.07.01-.13.03-.19l.08-.38c.15.28.45.48.8.48zm-18.27-1.01h10.36c.16 0 .28-.15.24-.31l-.38-1.5a.255.255 0 0 0-.24-.19h-9.6c-.11 0-.21.08-.24.19l-.38 1.5c-.04.16.08.31.24.31"/></g></svg>`
  },
  {
    id: "kmind-icon://builtin/collaboration/bell",
    group: "collaboration",
    name: "bell",
    label: "Reminder",
    catalog: { "groupId": "collaboration", "groupLabel": "People & Comms", "order": 140, "surfaces": ["node-content"] },
    viewBox: "0 0 32 32",
    svg: `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32" width="100%" height="100%" aria-hidden="true" focusable="false"><g fill="none"><path fill="#FF822D" d="M12.5 27.5c.448 1.442 1.838 2.5 3.5 2.5c1.663 0 3.052-1.058 3.5-2.5z"/><path fill="#FFB02E" d="M16 6.55c-.69 0-1.25-.56-1.25-1.25V3.25a1.25 1.25 0 0 1 2.5 0V5.3c0 .69-.56 1.25-1.25 1.25"/><path fill="#F9C23C" d="M27.6 22.843c-.96-.773-1.54-1.927-1.78-3.15l-1.73-8.9C23.32 6.85 19.94 4.01 16 4c-3.94.01-7.32 2.85-8.09 6.793l-1.73 8.9c-.24 1.223-.82 2.377-1.78 3.15a3.78 3.78 0 0 0-1.4 2.95v1.234c0 .542.43.973.95.973h24.1c.53 0 .95-.431.95-.973v-1.234c0-1.204-.55-2.258-1.4-2.95"/></g></svg>`
  },
  {
    id: "kmind-icon://builtin/collaboration/busts-in-silhouette",
    group: "collaboration",
    name: "busts-in-silhouette",
    label: "Team",
    catalog: { "groupId": "collaboration", "groupLabel": "People & Comms", "order": 140, "surfaces": ["node-content"] },
    viewBox: "0 0 32 32",
    svg: `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32" width="100%" height="100%" aria-hidden="true" focusable="false"><g fill="none"><path fill="#321B41" d="M15.84 23.93q.09.068.174.141q.084-.073.176-.141a11.07 11.07 0 0 1 12.65 0A2.91 2.91 0 0 1 30 26.29V30H2v-3.68a2.93 2.93 0 0 1 1.19-2.39a11.07 11.07 0 0 1 12.65 0"/><path fill="#533566" d="M10.67 7.93h-2.3a4.24 4.24 0 0 0-4.23 4.83l.067 1.022a1.71 1.71 0 0 0 .224 3.397l.099 1.501a4.05 4.05 0 0 0 3.15 3.427v.933a1.81 1.81 0 1 0 3.62 0v-.923a4.05 4.05 0 0 0 3.2-3.437l.094-1.503a1.71 1.71 0 0 0 1.396-.867a1.71 1.71 0 0 0 1.441.87l.099 1.5a4.05 4.05 0 0 0 3.15 3.427v.933a1.81 1.81 0 1 0 3.62 0v-.923a4.05 4.05 0 0 0 3.2-3.437l.094-1.503a1.71 1.71 0 0 0 .212-3.39l.064-1.027a4.26 4.26 0 0 0-4.2-4.83h-2.3a4.24 4.24 0 0 0-4.23 4.83l.067 1.022a1.71 1.71 0 0 0-1.217.848a1.71 1.71 0 0 0-1.184-.843l.064-1.027a4.26 4.26 0 0 0-4.2-4.83"/></g></svg>`
  },
  {
    id: "kmind-icon://builtin/collaboration/e-mail",
    group: "collaboration",
    name: "e-mail",
    label: "Email",
    catalog: { "groupId": "collaboration", "groupLabel": "People & Comms", "order": 140, "surfaces": ["node-content"] },
    viewBox: "0 0 32 32",
    svg: `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32" width="100%" height="100%" aria-hidden="true" focusable="false"><g fill="none"><rect width="30" height="22" x="1" y="5" fill="#B4ACBC" rx="1.5"/><rect width="28" height="18" x="2" y="7" fill="#CDC4D6" rx="1"/><path fill="#E1D8EC" d="m30 23.4l-12.971-7.782a2 2 0 0 0-2.058 0L2 23.4V25a1 1 0 0 0 1 1h26a1 1 0 0 0 1-1z"/><path fill="#998EA4" d="M2 9.766V8h28v1.766L17.544 17.24a3 3 0 0 1-3.088 0z"/><path fill="#F3EEF8" d="M2 8.6V7a1 1 0 0 1 1-1h26a1 1 0 0 1 1 1v1.6l-12.971 7.783a2 2 0 0 1-2.058 0z"/><path fill="#00A6ED" d="M16 23a7 7 0 1 0 0-14a7 7 0 0 0 0 14"/><path fill="#F4F4F4" d="M16 11.5c-1.21-.02-2.36.44-3.22 1.3c-.87.85-1.34 1.99-1.34 3.2c0 2.48 2.02 4.5 4.5 4.5a.47.47 0 1 0 0-.94c-1.96 0-3.56-1.6-3.56-3.56c0-.96.38-1.86 1.06-2.53s1.59-1.03 2.55-1.03c1.93.03 3.51 1.65 3.51 3.62v.81a.67.67 0 0 1-1.34 0v-3.08a.47.47 0 0 0-.47-.47c-.26 0-.49.21-.49.47v.09c-.44-.35-.99-.57-1.6-.57c-1.4 0-2.54 1.14-2.54 2.54s1.14 2.54 2.54 2.54c.7 0 1.34-.29 1.8-.75c.28.5.81.84 1.42.84c.89 0 1.62-.73 1.62-1.62v-.81c0-2.47-1.99-4.52-4.44-4.55m-.39 5.96c-.88 0-1.6-.72-1.6-1.6s.72-1.6 1.6-1.6s1.6.72 1.6 1.6s-.72 1.6-1.6 1.6"/></g></svg>`
  },
  {
    id: "kmind-icon://builtin/collaboration/handshake",
    group: "collaboration",
    name: "handshake",
    label: "Agreement",
    catalog: { "groupId": "collaboration", "groupLabel": "People & Comms", "order": 140, "surfaces": ["node-content"] },
    viewBox: "0 0 32 32",
    svg: `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32" width="100%" height="100%" aria-hidden="true" focusable="false"><g fill="none"><path fill="#FFC83D" d="M11.406 6.156c-5.275-.65-7.156 2-8.062 3.219c-2.469 3.64-.985 7.64.812 9.563c0 0 10.094 9.828 10.375 10.093s.946 1.172 2.547.914c1.398-.225 1.797-1.914 1.797-1.914s1.032.842 2.516 0c1.156-.656 1.109-1.968 1.109-1.968s1.238.62 2.563-.5c1.192-1.01.453-2.782.453-2.782s1.07.176 1.828-.656c1.025-1.125.672-2.547 0-3.187L19.625 10.5l-.594-3.125z"/><path fill="#D67D00" d="m26.707 22.593l-2.226-2.257a.5.5 0 1 0-.712.703l1.764 1.788l-.017-.046s.582.096 1.191-.188m-2.729 3.557l-2.31-2.563a.5.5 0 0 0-.743.67l1.66 1.841c.199.076.73.232 1.393.053m-3.402 2.2l-1.806-1.913a.5.5 0 1 0-.727.687l.904.957c.199.13.795.45 1.629.269m-2.173.703c-.759.202-2.167.265-3.137-.773l-.776.71l.041.04q.044.042.1.1c.328.34 1.01 1.046 2.447.814c.622-.1 1.046-.49 1.325-.892"/><path fill="#F59F00" d="M6.375 6.813c-1.687 2.166-4.287 7.775.313 11.625L5.24 19.993l-1.084-1.055C2.36 17.016.875 13.016 3.344 9.375l.04-.055c.525-.706 1.366-1.839 2.95-2.567z"/><path fill="#D67D00" d="M17.25 23.688c1.203 1.39-.3 3.162-1 3.906L5.669 16.584c1.974-2.002 3.278-2.203 4.16-1.334c.88.869.468 1.484.468 1.484s1.194-.678 2.453.563c1.26 1.241.39 2.187.39 2.187s1.3-.234 2.22.797c1.03 1.157.374 2.5.374 2.5s.79.068 1.516.907"/><path fill="#FFC83D" d="M12.438 8c3.234-1.297 8.14-1.953 10.39-1.984c1.531 0 3.481.37 5.547 2.797c3.3 3.874.828 8.296-1.125 10.093V17.5s-7.506-6.536-7.75-6.766c-.45-.425-2.302-.296-2.5-.234c-.604.188-1.65.5-3 1c-1.098.407-1.969.078-2.328-.766c-.36-.843-.842-2.09.765-2.734"/><path fill="#D67D00" d="M28.31 17.71a8.4 8.4 0 0 1-1.06 1.196c-2.76-2.406-8.378-7.325-8.828-7.75s-.974-.406-1.172-.344A79 79 79 0 0 0 13.75 12c-1.098.407-2.203-.422-2.562-1.266c-.33-.771-.356-1.879.87-2.556l.632-.277l.05-.019c-1.953 1.468-.228 3.262 1.385 3.056c.567-.073 1.5-.266 2.406-.5c.36-.094.713-.259 1.046-.414c.625-.293 1.18-.552 1.58-.243c1.5 1.165 5.976 4.968 9.154 7.929"/><path fill="#FFC83D" d="M8.82 16.879a2.203 2.203 0 0 0-3.09-.398L3.812 18.1c-.883.735-1.112 2.11-.467 3.002c.584.808 1.48 1.142 2.303.908c-.365.835-.334 1.903.367 2.49c.655.547 1.464.922 2.275.669c-.078.535.08 1.121.63 1.705c.52.551 1.276.826 2.087.643c-.107.572.074 1.208.743 1.853c.819.79 2.08.858 3.265-.23l.772-.9c.62-.78 1.478-2.136.196-3.288c-.443-.398-.952-.619-1.481-.62c.287-.7.282-1.558-.55-2.38c-.52-.513-1.157-.736-1.86-.568c.38-.808.371-1.633-.39-2.385c-.691-.683-1.543-1.007-2.643-.39c.194-.596.148-1.228-.24-1.731"/><path fill="#D67D00" d="M9.034 17.242L4.31 21.907c.418.186.873.229 1.31.112l3.469-3.426l-.029.016c.15-.459.156-.94-.026-1.367m3.212 2.584L6.96 25.085c.425.171.878.226 1.332.085l3.807-3.786l-.005.001c.245-.52.328-1.048.153-1.559m2.326 3.071l-4.918 4.498c.404.177.865.231 1.345.125l3.513-3.213c.17-.427.23-.912.06-1.41"/></g></svg>`
  },
  {
    id: "kmind-icon://builtin/collaboration/megaphone",
    group: "collaboration",
    name: "megaphone",
    label: "Announcement",
    catalog: { "groupId": "collaboration", "groupLabel": "People & Comms", "order": 140, "surfaces": ["node-content"] },
    viewBox: "0 0 32 32",
    svg: `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32" width="100%" height="100%" aria-hidden="true" focusable="false"><g fill="none"><path fill="#FFB02E" d="m25.064 23.405l-1.148-2.807l-1.715.702l1.15 2.81l.002.003a.755.755 0 0 1-.41.997l-4.906 2.012l-.003.001a.755.755 0 0 1-.996-.41l-1.152-2.815l-1.715.702l1.15 2.807a2.607 2.607 0 0 0 3.42 1.428h.002l4.894-2.008a2.607 2.607 0 0 0 1.428-3.42zM8 23.5l1.708 3.279c.62.65.59 1.68-.07 2.29c-.65.61-1.68.58-2.29-.07l-4.91-5.21c-.61-.65-.58-1.68.07-2.29s1.68-.58 2.29.07z"/><path fill="#F9C23C" d="m29.228 15.079l-11.55-12.25c-1.27-1.35-3.5-1-4.29.68l-8.59 18.06l4.97 5.27l18.54-7.51c1.71-.69 2.19-2.9.92-4.25"/></g></svg>`
  },
  {
    id: "kmind-icon://builtin/collaboration/speaking-head",
    group: "collaboration",
    name: "speaking-head",
    label: "Discussion",
    catalog: { "groupId": "collaboration", "groupLabel": "People & Comms", "order": 140, "surfaces": ["node-content"] },
    viewBox: "0 0 32 32",
    svg: `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32" width="100%" height="100%" aria-hidden="true" focusable="false"><path fill="#533566" d="M24.726 14.62c.445.467.66.692.724 1.23a1.79 1.79 0 0 1-1.83 1.98l.043.44c.05.491.097.967.097 1.43a.58.58 0 0 1-.55.59l-1.68.06a.38.38 0 0 0 0 .65l1.67 1.07a.77.77 0 0 1 .34.83c-.55 2.04-2.01 3.44-5.3 3.85q-.952.11-1.91.08a1.19 1.19 0 0 0-1.16.8l-.72 2h-10l2.18-6.89a2.76 2.76 0 0 0-.18-2.09C5.26 18.37 3.36 14.43 3.06 12a7.46 7.46 0 0 1 6.46-8.34l4.81-.6a7.47 7.47 0 0 1 8.31 6.47l.38 3a16 16 0 0 0 1.706 2.09m5.744 7.48v-1.94a.4.4 0 0 0-.51-.44l-3.24 1a.4.4 0 0 0 0 .76l3.24 1a.4.4 0 0 0 .51-.38M27.72 16l1.37 1.37A.4.4 0 0 1 29 18l-3 1.6a.4.4 0 0 1-.54-.53l1.6-3a.4.4 0 0 1 .66-.07m1.37 8.91l-1.37 1.37a.4.4 0 0 1-.66-.07l-1.6-3a.4.4 0 0 1 .54-.53l3 1.6a.4.4 0 0 1 .09.63"/></svg>`
  },
  {
    id: "kmind-icon://builtin/faces/angry-face",
    group: "faces",
    name: "angry-face",
    label: "Angry",
    catalog: { "groupId": "faces", "groupLabel": "Faces", "order": 170, "surfaces": ["node-content"] },
    viewBox: "0 0 32 32",
    svg: `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32" width="100%" height="100%" aria-hidden="true" focusable="false"><g fill="none"><path fill="#FFB02E" d="M15.999 29.998c9.334 0 13.999-6.268 13.999-14c0-7.73-4.665-13.998-14-13.998C6.665 2 2 8.268 2 15.999s4.664 13.999 13.999 13.999"/><path fill="#fff" d="M10.5 21a4.5 4.5 0 1 0 0-9a4.5 4.5 0 0 0 0 9m11 0a4.5 4.5 0 1 0 0-9a4.5 4.5 0 0 0 0 9"/><path fill="#402A32" d="M14.29 12.501a.75.75 0 0 1-.08 1.498c-1.017-.054-1.989-.304-2.817-.88c-.835-.582-1.46-1.452-1.854-2.631a.75.75 0 1 1 1.422-.476c.31.928.762 1.509 1.29 1.876c.534.372 1.21.569 2.039.613m3.42 0a.75.75 0 0 0 .08 1.498c1.017-.054 1.989-.304 2.817-.88c.835-.582 1.46-1.452 1.854-2.631a.75.75 0 1 0-1.422-.476c-.31.928-.763 1.509-1.29 1.876c-.534.372-1.21.569-2.039.613M16 24c-2.005 0-2.934 1.104-3.106 1.447a1 1 0 1 1-1.789-.894C11.602 23.563 13.205 22 16 22s4.4 1.562 4.894 2.553a1 1 0 1 1-1.788.894C18.934 25.104 18.005 24 16 24m-2-7a2 2 0 1 1-4 0a2 2 0 0 1 4 0m8 0a2 2 0 1 1-4 0a2 2 0 0 1 4 0"/></g></svg>`
  },
  {
    id: "kmind-icon://builtin/faces/beaming-face-with-smiling-eyes",
    group: "faces",
    name: "beaming-face-with-smiling-eyes",
    label: "Beaming",
    catalog: { "groupId": "faces", "groupLabel": "Faces", "order": 170, "surfaces": ["node-content"] },
    viewBox: "0 0 32 32",
    svg: `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32" width="100%" height="100%" aria-hidden="true" focusable="false"><g fill="none"><path fill="#FFB02E" d="M15.999 29.998c9.334 0 13.999-6.268 13.999-14c0-7.73-4.665-13.998-14-13.998C6.665 2 2 8.268 2 15.999s4.664 13.999 13.999 13.999"/><path fill="#402A32" d="M8.982 11.19c.048-.246.158-.55.367-.777c.18-.196.498-.413 1.15-.413c.643 0 .97.222 1.158.429c.218.24.323.545.358.742a1 1 0 0 0 1.97-.342a3.54 3.54 0 0 0-.85-1.747C12.563 8.452 11.696 8 10.5 8c-1.184 0-2.047.431-2.624 1.06c-.548.596-.769 1.293-.858 1.75a1 1 0 1 0 1.964.38m11 0c.048-.246.158-.55.367-.777c.18-.196.498-.413 1.151-.413c.642 0 .969.222 1.157.429c.219.24.324.545.358.742a1 1 0 0 0 1.97-.342a3.54 3.54 0 0 0-.85-1.747C23.563 8.452 22.696 8 21.5 8c-1.184 0-2.047.431-2.624 1.06c-.548.596-.769 1.293-.857 1.75a1 1 0 1 0 1.963.38"/><path fill="#BB1D80" d="M6 16h20s0 3.774-2.318 6.685H8.318C6 19.774 6 16 6 16"/><path fill="#fff" d="M7.759 19.794L7 16h18l-.759 3.794A1.5 1.5 0 0 1 22.771 21H9.23a1.5 1.5 0 0 1-1.471-1.206m.526 2.849C9.738 24.49 12.114 26 16 26s6.262-1.51 7.715-3.357A1 1 0 0 0 22.78 22H9.22a1 1 0 0 0-.935.643"/></g></svg>`
  },
  {
    id: "kmind-icon://builtin/faces/exploding-head",
    group: "faces",
    name: "exploding-head",
    label: "Mind Blown",
    catalog: { "groupId": "faces", "groupLabel": "Faces", "order": 170, "surfaces": ["node-content"] },
    viewBox: "0 0 32 32",
    svg: `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32" width="100%" height="100%" aria-hidden="true" focusable="false"><g fill="none"><path fill="#FFB02E" d="M16 30c9.33 0 14-6.26 14-13.979C30 11.947 25.34 10 16 10c-9.33 0-14 1.088-14 6.021C2 23.749 6.66 30 16 30"/><path fill="#fff" d="M14.93 20.46a4.48 4.48 0 1 1-8.96 0a4.48 4.48 0 0 1 8.96 0m11 0a4.48 4.48 0 1 1-8.96 0a4.48 4.48 0 0 1 8.96 0"/><path fill="#402A32" d="M13.97 20.94a2 2 0 1 1-4 0a2 2 0 0 1 4 0m8 0a2 2 0 1 1-4 0a2 2 0 0 1 4 0"/><path fill="#BB1D80" d="M15.97 28.91c-1.36 0-2.47-1.11-2.47-2.47s1.11-2.47 2.47-2.47s2.47 1.11 2.47 2.47s-1.11 2.47-2.47 2.47"/><path fill="#FF6723" d="M25.98 12.97c0 .987-3.073 1.8-8.02 1.968l-1.917-.829l-2.074.825c-4.89-.179-7.949-.993-7.949-1.964c0-1.1 3.92-2 10-2s9.96.9 9.96 2"/><path fill="#fff" d="M13.97 14.94c0-.718-.08-1.415-.23-2.072L16 9l2.193 3.874a9.5 9.5 0 0 0-.223 2.066z"/><path fill="#D3D3D3" d="M20.143 8.8A5 5 0 0 1 16 11a5 5 0 0 1-4.143-2.2A4 4 0 0 1 5 6c0-2.21 1.79-3.478 4-3.478c.68 0 1.32.17 1.882.47c.557.297 1.306.233 1.777-.19A4.98 4.98 0 0 1 16 1.522a4.98 4.98 0 0 1 3.341 1.28c.47.423 1.22.487 1.777.19A4 4 0 0 1 23 2.522c2.21 0 4 1.269 4 3.478a4 4 0 0 1-6.857 2.8"/><path fill="#E6E6E6" d="M27 6c0 .074-.106.079-.124.008a4.002 4.002 0 0 0-5.758-2.539c-.557.298-1.306.234-1.777-.189A4.98 4.98 0 0 0 16 2a4.98 4.98 0 0 0-3.341 1.28c-.47.423-1.22.487-1.777.19a4.002 4.002 0 0 0-5.758 2.538C5.106 6.078 5 6.074 5 6a4 4 0 0 1 5.882-3.53c.557.297 1.306.233 1.777-.19A4.98 4.98 0 0 1 16 1a4.98 4.98 0 0 1 3.341 1.28c.47.423 1.22.487 1.777.19A4 4 0 0 1 27 6"/><path fill="#C9C9C9" d="M16.859 12.38a1.65 1.65 0 0 0-1.718 0A4 4 0 0 1 9 9c0-2.21 1.79-3.458 4-3.458a4 4 0 0 1 2.141.621c.508.323 1.21.323 1.718 0A4 4 0 0 1 19 5.543c2.21 0 4 1.248 4 3.457a4 4 0 0 1-6.141 3.38"/><path fill="#fff" d="M23 9c0 .074-.106.079-.124.008a4.002 4.002 0 0 0-6.017-2.387a1.65 1.65 0 0 1-1.718 0a4.002 4.002 0 0 0-6.017 2.387C9.106 9.078 9 9.074 9 9a4 4 0 0 1 6.141-3.38c.508.323 1.21.323 1.718 0A4 4 0 0 1 23 9"/><path fill="#FFB02E" d="M7 4.5a1.5 1.5 0 1 1-3 0a1.5 1.5 0 0 1 3 0m17.38 2.26a1.38 1.38 0 1 0 0-2.76a1.38 1.38 0 0 0 0 2.76M5 9a1 1 0 1 1-2 0a1 1 0 0 1 2 0m23 1a1 1 0 1 1-2 0a1 1 0 0 1 2 0"/></g></svg>`
  },
  {
    id: "kmind-icon://builtin/faces/expressionless-face",
    group: "faces",
    name: "expressionless-face",
    label: "Blank",
    catalog: { "groupId": "faces", "groupLabel": "Faces", "order": 170, "surfaces": ["node-content"] },
    viewBox: "0 0 32 32",
    svg: `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32" width="100%" height="100%" aria-hidden="true" focusable="false"><g fill="none"><path fill="#FFB02E" d="M15.999 29.998c9.334 0 13.999-6.268 13.999-14c0-7.73-4.665-13.998-14-13.998C6.665 2 2 8.268 2 15.999s4.664 13.999 13.999 13.999"/><path fill="#402A32" d="M8 13a1 1 0 0 1 1-1h4a1 1 0 1 1 0 2H9a1 1 0 0 1-1-1m10 0a1 1 0 0 1 1-1h4a1 1 0 1 1 0 2h-4a1 1 0 0 1-1-1m-7 6a1 1 0 1 0 0 2h10a1 1 0 1 0 0-2z"/></g></svg>`
  },
  {
    id: "kmind-icon://builtin/faces/face-with-hand-over-mouth",
    group: "faces",
    name: "face-with-hand-over-mouth",
    label: "Surprised",
    catalog: { "groupId": "faces", "groupLabel": "Faces", "order": 170, "surfaces": ["node-content"] },
    viewBox: "0 0 32 32",
    svg: `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32" width="100%" height="100%" aria-hidden="true" focusable="false"><g fill="none"><path fill="#FFB02E" d="M15.999 29.998c9.334 0 13.999-6.268 13.999-14c0-7.73-4.665-13.998-14-13.998C6.665 2 2 8.268 2 15.999s4.664 13.999 13.999 13.999"/><path fill="#FF6723" d="M10 15c0 1.105-1.343 2-3 2s-3-.895-3-2s1.343-2 3-2s3 .895 3 2m18 0c0 1.105-1.343 2-3 2s-3-.895-3-2s1.343-2 3-2s3 .895 3 2"/><path fill="#402A32" d="M8.982 11.19c.048-.246.158-.55.367-.777c.18-.196.498-.413 1.15-.413c.643 0 .97.222 1.158.429c.218.24.323.545.358.742a1 1 0 0 0 1.97-.342a3.54 3.54 0 0 0-.85-1.747C12.563 8.452 11.696 8 10.5 8c-1.184 0-2.047.431-2.624 1.06c-.548.596-.769 1.293-.858 1.75a1 1 0 1 0 1.964.38m11 0c.048-.246.158-.55.367-.777c.18-.196.498-.413 1.151-.413c.642 0 .969.222 1.157.429c.219.24.324.545.358.742a1 1 0 0 0 1.97-.342a3.54 3.54 0 0 0-.85-1.747C23.563 8.452 22.696 8 21.5 8c-1.184 0-2.047.431-2.624 1.06c-.548.596-.769 1.293-.857 1.75a1 1 0 1 0 1.963.38"/><path fill="#FF822D" d="M16.043 17.689a1.25 1.25 0 0 0-1.927-1.573L11 19.232v-.982c0-.69-.56-1.25-1.25-1.25s-1.25.56-1.285 1.249C8.379 19.885 8.119 22.07 7.5 23c-1 1.5-1 4.5 1 6c3.816 2.862 8.334-2.018 8.741-2.473l2.643-2.643a1.25 1.25 0 0 0-.915-2.134l.354-.31a1.25 1.25 0 0 0-1.512-1.983l1.073-1.073a1.25 1.25 0 0 0-1.768-1.768z"/></g></svg>`
  },
  {
    id: "kmind-icon://builtin/faces/face-with-monocle",
    group: "faces",
    name: "face-with-monocle",
    label: "Inspect",
    catalog: { "groupId": "faces", "groupLabel": "Faces", "order": 170, "surfaces": ["node-content"] },
    viewBox: "0 0 32 32",
    svg: `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32" width="100%" height="100%" aria-hidden="true" focusable="false"><g fill="none"><path fill="#FFB02E" d="M15.999 29.998c9.334 0 13.999-6.268 13.999-14c0-7.73-4.665-13.998-14-13.998C6.665 2 2 8.268 2 15.999s4.664 13.999 13.999 13.999"/><path fill="#fff" d="M22 17.5a5.5 5.5 0 1 0 0-11a5.5 5.5 0 0 0 0 11M10.5 17a4.5 4.5 0 1 0 0-9a4.5 4.5 0 0 0 0 9"/><path fill="#9B9B9B" d="M28 12a6 6 0 1 0-1 3.318V25.5a.5.5 0 0 0 1 0zm-1 0v.004a5 5 0 1 1-10 0A5 5 0 0 1 27 12"/><path fill="#402A32" d="M18.777 4.916c.22-.146.637-.38 1.141-.575C20.425 4.145 20.985 4 21.5 4s1.075.145 1.582.341c.504.196.921.429 1.14.575a.5.5 0 0 0 .555-.832a7.3 7.3 0 0 0-1.334-.675C22.875 3.189 22.185 3 21.5 3s-1.375.188-1.943.409a7.3 7.3 0 0 0-1.334.675a.5.5 0 0 0 .554.832M7.916 6.777C8.183 6.377 9.11 5.5 10.5 5.5s2.317.877 2.584 1.277a.5.5 0 0 0 .832-.554c-.4-.6-1.606-1.723-3.416-1.723S7.484 5.623 7.084 6.223a.5.5 0 1 0 .832.554M15 19.75c-.835 0-1.23.393-1.293.457a1 1 0 0 1-1.414-1.414c.27-.27 1.142-1.043 2.707-1.043c2.4 0 4.234 1.483 4.894 2.803a1 1 0 1 1-1.788.894c-.34-.68-1.505-1.697-3.106-1.697M18 11a3 3 0 1 1 5.999-.001A3 3 0 0 1 18 11m-11 .5a3 3 0 1 1 5.999-.001A3 3 0 0 1 7 11.5"/></g></svg>`
  },
  {
    id: "kmind-icon://builtin/faces/face-with-open-mouth",
    group: "faces",
    name: "face-with-open-mouth",
    label: "Open Mouth",
    catalog: { "groupId": "faces", "groupLabel": "Faces", "order": 170, "surfaces": ["node-content"] },
    viewBox: "0 0 32 32",
    svg: `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32" width="100%" height="100%" aria-hidden="true" focusable="false"><g fill="none"><path fill="#FFB02E" d="M15.999 29.998c9.334 0 13.999-6.268 13.999-14c0-7.73-4.665-13.998-14-13.998C6.665 2 2 8.268 2 15.999s4.664 13.999 13.999 13.999"/><path fill="#fff" d="M10.5 16a4.5 4.5 0 1 0 0-9a4.5 4.5 0 0 0 0 9m11 0a4.5 4.5 0 1 0 0-9a4.5 4.5 0 0 0 0 9"/><path fill="#402A32" d="M12 14a2 2 0 1 0 0-4a2 2 0 0 0 0 4m8 0a2 2 0 1 0 0-4a2 2 0 0 0 0 4"/><path fill="#BB1D80" d="M12 22a4 4 0 0 1 8 0v2a4 4 0 0 1-8 0z"/></g></svg>`
  },
  {
    id: "kmind-icon://builtin/faces/face-with-rolling-eyes",
    group: "faces",
    name: "face-with-rolling-eyes",
    label: "Eye Roll",
    catalog: { "groupId": "faces", "groupLabel": "Faces", "order": 170, "surfaces": ["node-content"] },
    viewBox: "0 0 32 32",
    svg: `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32" width="100%" height="100%" aria-hidden="true" focusable="false"><g fill="none"><path fill="#FFB02E" d="M15.999 29.998c9.334 0 13.999-6.268 13.999-14c0-7.73-4.665-13.998-14-13.998C6.665 2 2 8.268 2 15.999s4.664 13.999 13.999 13.999"/><path fill="#fff" d="M10.5 19a4.5 4.5 0 0 0 2.463-8.266l-1.953.624l-1.803-1.17A4.502 4.502 0 0 0 10.5 19m11 0a4.5 4.5 0 0 0 1.293-8.811l-1.733 1.35l-2.012-.813A4.5 4.5 0 0 0 21.5 19"/><path fill="#402A32" d="M13 11a2 2 0 1 1-3.834-.799A4.5 4.5 0 0 1 10.5 10a4.5 4.5 0 0 1 2.484.747Q13 10.871 13 11m10 0a2 2 0 1 1-3.984-.253A4.5 4.5 0 0 1 21.5 10a4.5 4.5 0 0 1 1.334.201c.107.245.166.515.166.799M12 25a1 1 0 0 1 1-1h6a1 1 0 1 1 0 2h-6a1 1 0 0 1-1-1"/></g></svg>`
  },
  {
    id: "kmind-icon://builtin/faces/face-with-spiral-eyes",
    group: "faces",
    name: "face-with-spiral-eyes",
    label: "Dizzy",
    catalog: { "groupId": "faces", "groupLabel": "Faces", "order": 170, "surfaces": ["node-content"] },
    viewBox: "0 0 32 32",
    svg: `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32" width="100%" height="100%" aria-hidden="true" focusable="false"><g fill="none"><path fill="#FFB02E" d="M15.999 29.998c9.334 0 13.999-6.268 13.999-14c0-7.73-4.665-13.998-14-13.998C6.665 2 2 8.268 2 15.999s4.664 13.999 13.999 13.999"/><path fill="#402A32" d="M10.487 10.057c-2.193-.478-4.186 1.241-4.53 3.419a1 1 0 1 1-1.975-.312c.477-3.022 3.344-5.843 6.931-5.061a5.283 5.283 0 0 1 4.044 6.278A4.42 4.42 0 0 1 9.7 17.767a3.74 3.74 0 0 1-2.866-4.448v-.004c.18-.811.62-1.506 1.286-1.946c.669-.441 1.484-.572 2.308-.397c1.003.211 1.53 1.112 1.67 1.82c.074.382.068.83-.107 1.25a1.71 1.71 0 0 1-1.102.995a1 1 0 0 1-.751-1.843l-.003-.017a.5.5 0 0 0-.098-.217a.2.2 0 0 0-.034-.034c-.35-.072-.607-.003-.781.112c-.179.118-.353.338-.434.705a1.74 1.74 0 0 0 1.334 2.07a2.42 2.42 0 0 0 2.882-1.854a3.284 3.284 0 0 0-2.515-3.902zm-.49 2.866l.003.001zm1.943 8.724a1.5 1.5 0 0 1 2.12 0L16 23.586l1.94-1.94a1.5 1.5 0 0 1 2.12 0l1.94 1.94l1.793-1.793a1 1 0 0 1 1.414 1.414l-2.146 2.147a1.5 1.5 0 0 1-2.122 0L19 23.414l-1.94 1.94a1.5 1.5 0 0 1-2.12 0L13 23.414l-1.94 1.94a1.5 1.5 0 0 1-2.12 0l-2.147-2.147a1 1 0 1 1 1.414-1.414L10 23.586zm14.072-8.171c-.343-2.178-2.336-3.897-4.53-3.419a3.283 3.283 0 0 0-2.515 3.901a2.42 2.42 0 0 0 2.882 1.855a1.74 1.74 0 0 0 1.334-2.07c-.082-.367-.255-.587-.434-.705c-.175-.115-.43-.184-.782-.112a.2.2 0 0 0-.033.034a.5.5 0 0 0-.098.217l-.003.017a1 1 0 0 1-.751 1.843a1.71 1.71 0 0 1-1.102-.995a2.17 2.17 0 0 1-.107-1.25c.14-.708.667-1.609 1.67-1.82c.824-.175 1.64-.044 2.308.397c.666.44 1.107 1.135 1.285 1.946l.001.004a3.74 3.74 0 0 1-2.866 4.448a4.42 4.42 0 0 1-5.259-3.386a5.283 5.283 0 0 1 4.045-6.278c3.586-.782 6.454 2.039 6.93 5.061a1 1 0 1 1-1.975.312m-4.04-.553"/></g></svg>`
  },
  {
    id: "kmind-icon://builtin/faces/face-with-tears-of-joy",
    group: "faces",
    name: "face-with-tears-of-joy",
    label: "Joy",
    catalog: { "groupId": "faces", "groupLabel": "Faces", "order": 170, "surfaces": ["node-content"] },
    viewBox: "0 0 32 32",
    svg: `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32" width="100%" height="100%" aria-hidden="true" focusable="false"><g fill="none"><path fill="#FFB02E" d="M15.999 29.998c9.334 0 13.999-6.268 13.999-14c0-7.73-4.665-13.998-14-13.998C6.665 2 2 8.268 2 15.999s4.664 13.999 13.999 13.999"/><path fill="#402A32" d="M8.982 11.19c.048-.246.158-.55.367-.777c.18-.196.498-.413 1.15-.413c.643 0 .97.222 1.158.429c.218.24.323.545.358.742a1 1 0 0 0 1.97-.342a3.54 3.54 0 0 0-.85-1.747C12.563 8.452 11.696 8 10.5 8c-1.184 0-2.047.431-2.624 1.06c-.548.596-.769 1.293-.858 1.75a1 1 0 1 0 1.964.38m11 0c.048-.246.158-.55.367-.777c.18-.196.498-.413 1.151-.413c.642 0 .969.222 1.157.429c.219.24.324.545.358.742a1 1 0 0 0 1.97-.342a3.54 3.54 0 0 0-.85-1.747C23.563 8.452 22.696 8 21.5 8c-1.184 0-2.047.431-2.624 1.06c-.548.596-.769 1.293-.857 1.75a1 1 0 1 0 1.963.38"/><path fill="#BB1D80" d="M16 25c-9 0-9-9-9-9h18s0 9-9 9"/><path fill="#fff" d="M8 16.5V16h16v.5a1 1 0 0 1-1 1H9a1 1 0 0 1-1-1"/><path fill="#3F5FFF" d="M4.63 20.37L8 17a2.121 2.121 0 1 0-3-3l-3.37 3.37a2.121 2.121 0 1 0 3 3m22.99 0L24.25 17a2.121 2.121 0 0 1 3-3l3.37 3.37a2.121 2.121 0 0 1-3 3"/></g></svg>`
  },
  {
    id: "kmind-icon://builtin/faces/grinning-face",
    group: "faces",
    name: "grinning-face",
    label: "Grinning",
    catalog: { "groupId": "faces", "groupLabel": "Faces", "order": 170, "surfaces": ["node-content"] },
    viewBox: "0 0 32 32",
    svg: `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32" width="100%" height="100%" aria-hidden="true" focusable="false"><g fill="none"><path fill="#FFB02E" d="M15.999 29.998c9.334 0 13.999-6.268 13.999-14c0-7.73-4.665-13.998-14-13.998C6.665 2 2 8.268 2 15.999s4.664 13.999 13.999 13.999"/><path fill="#fff" d="M15 10.5a4.5 4.5 0 0 1-1.694 3.518c-.803-.27-1.83-.518-2.806-.518c-.977 0-2.003.248-2.806.518A4.5 4.5 0 1 1 15 10.5m11 0a4.5 4.5 0 0 1-1.694 3.518c-.803-.27-1.83-.518-2.806-.518c-.977 0-2.003.248-2.806.518A4.5 4.5 0 1 1 26 10.5"/><path fill="#402A32" d="M11 13a3 3 0 1 0 0-6a3 3 0 0 0 0 6m10 0a3 3 0 1 0 0-6a3 3 0 0 0 0 6"/><path fill="#BB1D80" d="M16 25c-9 0-9-9-9-9h18s0 9-9 9"/><path fill="#fff" d="M8 16.5V16h16v.5a1 1 0 0 1-1 1H9a1 1 0 0 1-1-1"/></g></svg>`
  },
  {
    id: "kmind-icon://builtin/faces/loudly-crying-face",
    group: "faces",
    name: "loudly-crying-face",
    label: "Crying",
    catalog: { "groupId": "faces", "groupLabel": "Faces", "order": 170, "surfaces": ["node-content"] },
    viewBox: "0 0 32 32",
    svg: `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32" width="100%" height="100%" aria-hidden="true" focusable="false"><g fill="none"><path fill="#FFB02E" d="M15.999 29.998c9.334 0 13.999-6.268 13.999-14c0-7.73-4.665-13.998-14-13.998C6.665 2 2 8.268 2 15.999s4.664 13.999 13.999 13.999"/><path fill="#5092FF" d="M11 29.297V8H7.5A1.5 1.5 0 0 0 6 9.5v16.91c1.333 1.28 3 2.273 5 2.887m15-2.89c-1.333 1.282-3 2.275-5 2.89V8h3.5A1.5 1.5 0 0 1 26 9.5z"/><path fill="#402A32" d="M6.949 9.316c.048-.145.435-.816 1.551-.816s1.503.67 1.551.816a1 1 0 0 0 1.898-.632C11.664 7.829 10.585 6.5 8.5 6.5S5.336 7.83 5.051 8.684a1 1 0 0 0 1.898.632m15 0c.048-.145.435-.816 1.551-.816s1.503.67 1.551.816a1 1 0 0 0 1.898-.632C26.664 7.829 25.584 6.5 23.5 6.5s-3.164 1.33-3.449 2.184a1 1 0 0 0 1.898.632"/><path fill="#BB1D80" d="M12 15a4 4 0 0 1 8 0v2a4 4 0 0 1-8 0z"/></g></svg>`
  },
  {
    id: "kmind-icon://builtin/faces/neutral-face",
    group: "faces",
    name: "neutral-face",
    label: "Neutral",
    catalog: { "groupId": "faces", "groupLabel": "Faces", "order": 170, "surfaces": ["node-content"] },
    viewBox: "0 0 32 32",
    svg: `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32" width="100%" height="100%" aria-hidden="true" focusable="false"><g fill="none"><path fill="#FFB02E" d="M15.999 29.998c9.334 0 13.999-6.268 13.999-14c0-7.73-4.665-13.998-14-13.998C6.665 2 2 8.268 2 15.999s4.664 13.999 13.999 13.999"/><path fill="#fff" d="M10.42 16.224a4.206 4.206 0 1 0 0-8.411a4.206 4.206 0 0 0 0 8.411m11.148.077a4.244 4.244 0 1 0 0-8.489a4.244 4.244 0 0 0 0 8.49"/><path fill="#402A32" d="M11 15a3 3 0 1 0 0-6a3 3 0 0 0 0 6m10 0a3 3 0 1 0 0-6a3 3 0 0 0 0 6m-11 5a1 1 0 0 1 1-1h10a1 1 0 1 1 0 2H11a1 1 0 0 1-1-1"/></g></svg>`
  },
  {
    id: "kmind-icon://builtin/faces/pleading-face",
    group: "faces",
    name: "pleading-face",
    label: "Pleading",
    catalog: { "groupId": "faces", "groupLabel": "Faces", "order": 170, "surfaces": ["node-content"] },
    viewBox: "0 0 32 32",
    svg: `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32" width="100%" height="100%" aria-hidden="true" focusable="false"><g fill="none"><path fill="#FFB02E" d="M15.999 29.998c9.334 0 13.999-6.268 13.999-14c0-7.73-4.665-13.998-14-13.998C6.665 2 2 8.268 2 15.999s4.664 13.999 13.999 13.999"/><path fill="#fff" d="M15 16.5a4.5 4.5 0 1 1-9 0a4.5 4.5 0 0 1 9 0m10.96-.02a4.48 4.48 0 1 1-8.96 0a4.48 4.48 0 0 1 8.96 0"/><path fill="#402A32" d="M10.88 12C8.74 12 7 13.74 7 15.88s1.74 3.88 3.88 3.88s3.88-1.74 3.88-3.88S13.02 12 10.88 12m10 0C18.74 12 17 13.74 17 15.88s1.74 3.88 3.88 3.88s3.88-1.74 3.88-3.88S23.02 12 20.88 12"/><path fill="#fff" d="M13.163 15.937c.745-.237 1.049-1.07.68-1.865c-.367-.788-1.26-1.246-2.006-1.01c-.745.238-1.049 1.07-.68 1.866c.367.795 1.26 1.246 2.006 1.009m10 0c.745-.237 1.049-1.07.68-1.865c-.367-.788-1.27-1.246-2.006-1.01c-.745.238-1.049 1.07-.68 1.866c.367.795 1.26 1.246 2.006 1.009"/><path fill="#402A32" d="M8.952 9.2c.54-.475.875-1.127 1.065-1.83a.5.5 0 0 1 .966.26c-.225.831-.64 1.68-1.371 2.321C8.873 10.6 7.855 11 6.5 11a.5.5 0 0 1 0-1c1.145 0 1.92-.333 2.452-.8m5.944 16.245q-.003.005-.002.002a1 1 0 1 1-1.788-.894C13.434 23.896 14.405 23 16 23s2.566.896 2.894 1.553a1 1 0 1 1-1.788.894l-.002-.002c-.013-.018-.086-.12-.251-.225c-.173-.11-.447-.22-.853-.22s-.68.11-.853.22a.9.9 0 0 0-.25.225M21.983 7.37c.19.703.525 1.355 1.065 1.83c.533.467 1.307.8 2.452.8a.5.5 0 0 1 0 1c-1.355 0-2.373-.4-3.112-1.049c-.73-.642-1.146-1.49-1.37-2.32a.5.5 0 1 1 .965-.262"/></g></svg>`
  },
  {
    id: "kmind-icon://builtin/faces/saluting-face",
    group: "faces",
    name: "saluting-face",
    label: "Salute",
    catalog: { "groupId": "faces", "groupLabel": "Faces", "order": 170, "surfaces": ["node-content"] },
    viewBox: "0 0 32 32",
    svg: `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32" width="100%" height="100%" aria-hidden="true" focusable="false"><g fill="none"><path fill="#FFB02E" d="M18.297 30c8.002 0 12-5.373 12-12s-3.998-12-12-12s-12 5.373-12 12s3.999 12 12 12"/><path fill="#fff" d="M13.514 18.194a3.605 3.605 0 1 0 0-7.211a3.605 3.605 0 0 0 0 7.21m9.557.067a3.638 3.638 0 1 0 0-7.277a3.638 3.638 0 0 0 0 7.276"/><path fill="#402A32" d="M16.584 14.573a2.572 2.572 0 1 1-5.144 0a2.572 2.572 0 0 1 5.144 0m8.572 0a2.572 2.572 0 1 1-5.143 0a2.572 2.572 0 0 1 5.143 0M14.9 20.178a.75.75 0 0 0-1.213.883c.548.751 2.147 2.152 4.45 2.152c2.282 0 4.093-1.38 4.741-2.087a.75.75 0 0 0-1.107-1.013c-.477.522-1.916 1.6-3.634 1.6c-1.697 0-2.889-1.057-3.237-1.535"/><path fill="#FF822D" d="M14.785 2.637c.115-.07.232-.14.359-.183l.555.242l.222.959a1.048 1.048 0 0 1 .6 1.953l-3.9 2.252a1.062 1.062 0 0 1 .912 1.9l-2.415 1.344a6.34 6.34 0 0 1-3.415.999H4.795l2.978-4.839c-.435-.773-.82-1.483-.82-1.483l4.55-2.67l.455-.263l2.728-.152z"/><path fill="#FFB02E" d="M10.235 2.943a1.05 1.05 0 0 1 1.267.168l1.674-.966a1.048 1.048 0 0 1 1.51.55l.27-.156a1.048 1.048 0 0 1 1.05 1.815L9.367 8.186q.132-.451.173-.928l4.94-2.852c.688-.397.96-1.238.663-1.952q-.097.033-.187.085l-.271.156a1.05 1.05 0 0 1-.462 1.265L9.558 6.654V6.35l1.983-1.145a1.563 1.563 0 0 0 .417-2.357l-.456.263q.095.095.165.216c.29.501.118 1.142-.383 1.432L8.989 6.084v.079q0 .266-.024.529l-.003.039a6 6 0 0 1-.485 1.857a6 6 0 0 1-2.323 2.672l-1.359.843A2.795 2.795 0 0 1 2 9.308v-.072c0-1.058.583-2.03 1.517-2.529l2.36-1.26l-.003.014z"/></g></svg>`
  },
  {
    id: "kmind-icon://builtin/faces/shushing-face",
    group: "faces",
    name: "shushing-face",
    label: "Shh",
    catalog: { "groupId": "faces", "groupLabel": "Faces", "order": 170, "surfaces": ["node-content"] },
    viewBox: "0 0 32 32",
    svg: `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32" width="100%" height="100%" aria-hidden="true" focusable="false"><g fill="none"><path fill="#FFB02E" d="M15.999 29.998c9.334 0 13.999-6.268 13.999-14c0-7.73-4.665-13.998-14-13.998C6.665 2 2 8.268 2 15.999s4.664 13.999 13.999 13.999"/><path fill="#fff" d="M10.42 16.224a4.206 4.206 0 1 0 0-8.411a4.206 4.206 0 0 0 0 8.411m11.148.077a4.244 4.244 0 1 0 0-8.489a4.244 4.244 0 0 0 0 8.49"/><path fill="#402A32" d="M14 12a3 3 0 1 1-6 0a3 3 0 0 1 6 0m10 0a3 3 0 1 1-6 0a3 3 0 0 1 6 0m-11 8a1 1 0 1 0 0 2h6a1 1 0 1 0 0-2z"/><path fill="#FF822D" d="M18.79 22.02c-.77 0-.77-.77-.77-.77v-3.23c0-1.1-.9-2-2-2s-2 .9-2 2v9.7c0 2.34 1.9 4.23 4.23 4.23h.53c2.34 0 4.23-1.9 4.23-4.23v-1.47c.01-2.33-1.71-4.23-4.22-4.23"/></g></svg>`
  },
  {
    id: "kmind-icon://builtin/faces/slightly-smiling-face",
    group: "faces",
    name: "slightly-smiling-face",
    label: "Smiling",
    catalog: { "groupId": "faces", "groupLabel": "Faces", "order": 170, "surfaces": ["node-content"] },
    viewBox: "0 0 32 32",
    svg: `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32" width="100%" height="100%" aria-hidden="true" focusable="false"><g fill="none"><path fill="#FFB02E" d="M15.999 29.998c9.334 0 13.999-6.268 13.999-14c0-7.73-4.665-13.998-14-13.998C6.665 2 2 8.268 2 15.999s4.664 13.999 13.999 13.999"/><path fill="#fff" d="M10.42 16.224a4.206 4.206 0 1 0 0-8.411a4.206 4.206 0 0 0 0 8.411m11.148.077a4.244 4.244 0 1 0 0-8.489a4.244 4.244 0 0 0 0 8.49"/><path fill="#402A32" d="M11 15a3 3 0 1 0 0-6a3 3 0 0 0 0 6m10 0a3 3 0 1 0 0-6a3 3 0 0 0 0 6"/><path fill="#402A32" fill-rule="evenodd" d="M10.4 18.2a1 1 0 0 1 1.4.2c.31.413 1.712 1.6 4.2 1.6s3.89-1.187 4.2-1.6a1 1 0 1 1 1.6 1.2c-.69.92-2.688 2.4-5.8 2.4s-5.11-1.48-5.8-2.4a1 1 0 0 1 .2-1.4" clip-rule="evenodd"/></g></svg>`
  },
  {
    id: "kmind-icon://builtin/faces/smiling-face-with-sunglasses",
    group: "faces",
    name: "smiling-face-with-sunglasses",
    label: "Cool",
    catalog: { "groupId": "faces", "groupLabel": "Faces", "order": 170, "surfaces": ["node-content"] },
    viewBox: "0 0 32 32",
    svg: `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32" width="100%" height="100%" aria-hidden="true" focusable="false"><g fill="none"><path fill="#FFB02E" d="M15.999 29.998c9.334 0 13.999-6.268 13.999-14c0-7.73-4.665-13.998-14-13.998C6.665 2 2 8.268 2 15.999s4.664 13.999 13.999 13.999"/><path fill="#402A32" d="M11.84 18.457a1 1 0 0 0-1.688 1.073l.001.002l.002.003l.004.006l.009.013a2 2 0 0 0 .097.137c.06.08.147.185.26.306c.226.241.563.546 1.03.845C12.5 21.446 13.937 22 16 22s3.5-.554 4.445-1.158a5.4 5.4 0 0 0 1.03-.845a4 4 0 0 0 .357-.443l.01-.013l.003-.006l.001-.002l.001-.001v-.002a1 1 0 0 0-1.686-1.073l-.018.024a2 2 0 0 1-.126.147a3.4 3.4 0 0 1-.65.53c-.62.396-1.682.842-3.367.842s-2.748-.446-3.367-.842a3.4 3.4 0 0 1-.65-.53a2 2 0 0 1-.144-.171"/><path fill="#321B41" d="M11 5H5a4 4 0 0 0-4 4v.674a7 7 0 0 0 3.87 6.26l.935.469a5.8 5.8 0 0 0 4.52.267C13.111 15.675 15 13.025 15 10.067V9a4 4 0 0 0-4-4m9.5 0h7A3.5 3.5 0 0 1 31 8.5v1.174a7 7 0 0 1-3.87 6.26l-.935.469a5.8 5.8 0 0 1-4.52.267C18.889 15.675 17 13.025 17 10.067V8.5A3.5 3.5 0 0 1 20.5 5"/><path fill="#8D65C5" d="M14 6.354A4 4 0 0 0 11 5H5a4 4 0 0 0-4 4v.674a7 7 0 0 0 3.87 6.26l.935.469a5.8 5.8 0 0 0 4.52.267C13.111 15.675 15 13.025 15 10.067V10a1 1 0 1 1 2 0v.067c0 2.958 1.889 5.608 4.675 6.603a5.8 5.8 0 0 0 4.52-.267l.936-.468A7 7 0 0 0 31 9.674V8.5A3.5 3.5 0 0 0 27.5 5h-7c-1.124 0-2.124.53-2.765 1.354V6.35l-.05.05c-.191.197-.582.596-.945.599h-1.744c-.364-.003-.754-.402-.946-.599L14 6.35zM11 6a3 3 0 0 1 3 3v1.067c0 2.53-1.618 4.806-4.011 5.66a4.8 4.8 0 0 1-3.736-.219l-.936-.468A6 6 0 0 1 2 9.674V9a3 3 0 0 1 3-3zm7 2.5A2.5 2.5 0 0 1 20.5 6h7A2.5 2.5 0 0 1 30 8.5v1.174a6 6 0 0 1-3.317 5.366l-.936.468a4.78 4.78 0 0 1-3.736.22C19.618 14.873 18 12.598 18 10.067z"/><path fill="#fff" d="M12.39 10.268c.585-.586.427-1.694-.354-2.475s-1.89-.94-2.475-.354s-.428 1.694.353 2.475s1.89.94 2.475.354m16.001 0c.585-.586.427-1.694-.354-2.475c-.782-.781-1.89-.94-2.475-.354s-.428 1.694.353 2.475s1.89.94 2.475.354"/></g></svg>`
  },
  {
    id: "kmind-icon://builtin/faces/star-struck",
    group: "faces",
    name: "star-struck",
    label: "Star-struck",
    catalog: { "groupId": "faces", "groupLabel": "Faces", "order": 170, "surfaces": ["node-content"] },
    viewBox: "0 0 32 32",
    svg: `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32" width="100%" height="100%" aria-hidden="true" focusable="false"><g fill="none"><path fill="#FFB02E" d="M15.999 29.998c9.334 0 13.999-6.268 13.999-14c0-7.73-4.665-13.998-14-13.998C6.665 2 2 8.268 2 15.999s4.664 13.999 13.999 13.999"/><path fill="#BB1D80" d="m5.727 15.434l3.05-2.372a2 2 0 0 1 1.62-.382l3.65.73a.25.25 0 0 0 .282-.338l-1.412-3.528a2 2 0 0 1 .257-1.943L14.96 5.22a.4.4 0 0 0-.356-.639L11.11 4.9a2 2 0 0 1-1.78-.792l-1.365-1.82a.72.72 0 0 0-1.282.291l-.472 2.359a2 2 0 0 1-1.218 1.464l-2.53 1.012a.75.75 0 0 0-.085 1.352l1.983 1.102a2 2 0 0 1 1.02 1.929l-.299 3.285a.4.4 0 0 0 .644.352m20.547 0l-3.05-2.372a2 2 0 0 0-1.62-.382l-3.65.73a.25.25 0 0 1-.282-.338l1.412-3.528a2 2 0 0 0-.257-1.943L17.04 5.22a.4.4 0 0 1 .356-.639l3.492.318a2 2 0 0 0 1.782-.792l1.364-1.819a.72.72 0 0 1 1.282.291l.472 2.359a2 2 0 0 0 1.218 1.464l2.53 1.012a.75.75 0 0 1 .085 1.352l-1.983 1.102a2 2 0 0 0-1.02 1.929l.299 3.285a.4.4 0 0 1-.644.352M16 26c-9 0-9-9-9-9h18s0 9-9 9"/><path fill="#fff" d="M8 17.5V17h16v.5a1 1 0 0 1-1 1H9a1 1 0 0 1-1-1"/></g></svg>`
  },
  {
    id: "kmind-icon://builtin/faces/thinking-face",
    group: "faces",
    name: "thinking-face",
    label: "Thinking",
    catalog: { "groupId": "faces", "groupLabel": "Faces", "order": 170, "surfaces": ["node-content"] },
    viewBox: "0 0 32 32",
    svg: `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32" width="100%" height="100%" aria-hidden="true" focusable="false"><g fill="none"><path fill="#FFB02E" d="M15.999 29.998c9.334 0 13.999-6.268 13.999-14c0-7.73-4.665-13.998-14-13.998C6.665 2 2 8.268 2 15.999s4.664 13.999 13.999 13.999"/><path fill="#FFB02E" d="M10 21.5v-3.06A1.44 1.44 0 0 0 8.56 17c-.84 0-1.505.718-1.517 1.559C7.023 19.92 6.835 21.722 6 22c-3 1-4 5.5-1.5 7.5c2 1.6 4 1.5 5.5 1.5h2.764a1.236 1.236 0 0 0 .553-2.342L13 28.5h.72a1 1 0 0 0 .97-.758l.067-.272A.78.78 0 0 0 14 26.5l.33-.165a1.214 1.214 0 0 0 0-2.17L14 24h1.75a1.25 1.25 0 1 0 0-2.5z"/><path fill="#fff" d="M10.42 16.224a4.206 4.206 0 1 0 0-8.411a4.206 4.206 0 0 0 0 8.411m11.148.077a4.244 4.244 0 1 0 0-8.489a4.244 4.244 0 0 0 0 8.49"/><path fill="#FF822D" d="M10 21.5v-3.06A1.44 1.44 0 0 0 8.56 17c-.84 0-1.505.718-1.517 1.559C7.023 19.92 6.835 21.722 6 22c-3 1-4 5.5-1.5 7.5c2 1.6 4 1.5 5.5 1.5h2.764a1.236 1.236 0 0 0 .553-2.342L13 28.5h.72a1 1 0 0 0 .97-.758l.067-.272A.78.78 0 0 0 14 26.5l.33-.165a1.214 1.214 0 0 0 0-2.17L14 24h1.75a1.25 1.25 0 1 0 0-2.5z"/><path fill="#402A32" d="M7.146 4.146C7.543 3.75 8.63 3 10 3s2.457.75 2.854 1.146a.5.5 0 0 1-.708.708C11.876 4.584 11.03 4 10 4s-1.877.584-2.146.854a.5.5 0 1 1-.708-.708m11.034 3.97C18.65 7.724 19.92 7 21.5 7s2.85.724 3.32 1.116a.5.5 0 0 1-.64.768C23.85 8.61 22.8 8 21.5 8s-2.35.61-2.68.884a.5.5 0 0 1-.64-.768M13 11.5a3 3 0 1 1-6 0a3 3 0 0 1 6 0"/><path fill="#402A32" d="M24 11.5a3 3 0 1 1-6 0a3 3 0 0 1 6 0m-7.919 7.486a2.73 2.73 0 0 0-2.374.721a1 1 0 0 1-1.414-1.414a4.73 4.73 0 0 1 4.126-1.279c1.962.336 2.973 1.457 3.488 2.565a1 1 0 0 1-1.814.842c-.28-.604-.791-1.227-2.012-1.435"/></g></svg>`
  },
  {
    id: "kmind-icon://builtin/focus/bullseye",
    group: "focus",
    name: "bullseye",
    label: "Goal",
    catalog: { "groupId": "focus", "groupLabel": "Focus & Goals", "order": 160, "surfaces": ["node-content"] },
    viewBox: "0 0 32 32",
    svg: `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32" width="100%" height="100%" aria-hidden="true" focusable="false"><g fill="none"><path fill="#F4F4F4" d="M14 28.292c5.684 0 10.292-4.608 10.292-10.292S19.684 7.708 14 7.708S3.708 12.316 3.708 18S8.316 28.292 14 28.292"/><path fill="#F8312F" d="M26 18c0-6.627-5.373-12-12-12S2 11.373 2 18s5.373 12 12 12s12-5.373 12-12m-3 0a9 9 0 1 1-18 0a9 9 0 0 1 18 0m-9 6a6 6 0 1 1 0-12a6 6 0 0 1 0 12m3-6a3 3 0 1 0-6 0a3 3 0 0 0 6 0"/><path fill="#9B9B9B" d="M14.25 17.742a.864.864 0 0 0 1.232 0l4.26-4.254a.86.86 0 0 0 0-1.23a.864.864 0 0 0-1.232 0l-4.26 4.254a.88.88 0 0 0 0 1.23"/><path fill="#46A4FB" d="m19.658 10.093l-.45-1.59c-.54-1.9-.01-3.95 1.39-5.34l.89-.89a.906.906 0 0 1 1.52.39L24 6zM22 12.33l1.572.458c1.878.55 3.904.01 5.278-1.416l.88-.906c.494-.5.277-1.356-.385-1.55L26 8z"/><path fill="#50E2FF" d="M15.85 16.152a2.892 2.892 0 0 0 4.307-.24l5.424-6.798a1.92 1.92 0 0 0-2.698-2.696l-6.802 5.42a2.904 2.904 0 0 0-.231 4.314"/><path fill="#46A4FB" d="M21.258 10.742a.86.86 0 0 0 1.23 0l4.254-4.254a.86.86 0 0 0 0-1.23a.86.86 0 0 0-1.23 0l-4.254 4.254a.86.86 0 0 0 0 1.23"/></g></svg>`
  },
  {
    id: "kmind-icon://builtin/focus/gear",
    group: "focus",
    name: "gear",
    label: "System",
    catalog: { "groupId": "focus", "groupLabel": "Focus & Goals", "order": 160, "surfaces": ["node-content"] },
    viewBox: "0 0 32 32",
    svg: `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32" width="100%" height="100%" aria-hidden="true" focusable="false"><g fill="none"><path fill="#B4ACBC" d="M12.847 3.834A2 2 0 0 1 14.84 2h2.32a2 2 0 0 1 1.993 1.834l.235 2.825a.5.5 0 0 0 .821.34l2.164-1.831a2 2 0 0 1 2.706.112l1.64 1.64a2 2 0 0 1 .113 2.707l-1.83 2.163a.5.5 0 0 0 .34.822l2.824.235A2 2 0 0 1 30 14.84v2.32a2 2 0 0 1-1.834 1.993l-2.825.235a.5.5 0 0 0-.34.821l1.831 2.164a2 2 0 0 1-.112 2.706l-1.64 1.64a2 2 0 0 1-2.707.113l-2.164-1.83a.5.5 0 0 0-.82.34l-.236 2.824A2 2 0 0 1 17.16 30h-2.32a2 2 0 0 1-1.993-1.834l-.235-2.825a.5.5 0 0 0-.822-.34l-2.163 1.831a2 2 0 0 1-2.706-.112l-1.64-1.64a2 2 0 0 1-.113-2.707l1.83-2.164a.5.5 0 0 0-.34-.82l-2.824-.236A2 2 0 0 1 2 17.16v-2.32a2 2 0 0 1 1.834-1.993l2.825-.235a.5.5 0 0 0 .34-.822L5.168 9.628A2 2 0 0 1 5.28 6.92l1.64-1.64a2 2 0 0 1 2.707-.113l2.163 1.83a.5.5 0 0 0 .822-.34zM21 16a5 5 0 1 0-10 0a5 5 0 0 0 10 0"/><path fill="#998EA4" d="M24 16a8 8 0 1 1-16 0a8 8 0 0 1 16 0m-3.5 0a4.5 4.5 0 1 0-9 0a4.5 4.5 0 0 0 9 0"/><path fill="#CDC4D6" d="M10.5 16a5.5 5.5 0 1 1 11 0a5.5 5.5 0 0 1-11 0M21 16a5 5 0 1 0-10 0a5 5 0 0 0 10 0"/></g></svg>`
  },
  {
    id: "kmind-icon://builtin/focus/puzzle-piece",
    group: "focus",
    name: "puzzle-piece",
    label: "Strategy",
    catalog: { "groupId": "focus", "groupLabel": "Focus & Goals", "order": 160, "surfaces": ["node-content"] },
    viewBox: "0 0 32 32",
    svg: `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32" width="100%" height="100%" aria-hidden="true" focusable="false"><g fill="none"><path fill="#D3D3D3" d="m23.623 21.425l.995.996a1.37 1.37 0 0 0 1.94 0l3.143-3.147a1.01 1.01 0 0 0 0-1.434l-5.83-5.837a.445.445 0 0 1 0-.637c.11-.11.26-.15.399-.12c.945.16 1.95-.12 2.676-.846a3.07 3.07 0 0 0-.03-4.362l-.856-.867l-.388.13a3.05 3.05 0 0 0-3.89 3.406c.02.15-.02.289-.129.398l-.02.02a.444.444 0 0 1-.636 0L15.167 3.3a1.01 1.01 0 0 0-1.433 0l-3.113 3.117c-.08.08-.14.17-.2.259l-.208-.21l-.737.738l1.144 1.145l.02.02c.279.279.657.428 1.045.408a3.06 3.06 0 0 1 2.457 1.056a3.07 3.07 0 0 1 0 4.004a3.06 3.06 0 0 1-4.477.17a3.01 3.01 0 0 1-.885-2.351c.02-.389-.12-.767-.398-1.046a.1.1 0 0 0-.03-.04l-.975-.976l-.427.438l.189.19a1.34 1.34 0 0 0-.697.378l-3.144 3.147a1.01 1.01 0 0 0 0 1.434l5.84 5.847c.18.179.18.458 0 .637a.43.43 0 0 1-.398.12a3.06 3.06 0 0 0-2.815.995a3.07 3.07 0 0 0-.01 4.014a3.05 3.05 0 0 0 4.477.16a3.06 3.06 0 0 0 .855-2.64a.46.46 0 0 1 .13-.398l.02-.02a.444.444 0 0 1 .636 0l5.8 5.806a1.01 1.01 0 0 0 1.433 0l3.114-3.117a1.37 1.37 0 0 0 0-1.942l-.02-.02l-.886-.887l-.388.389l.11.11a3.07 3.07 0 0 1-2.328-1.056a3.07 3.07 0 0 1 0-4.004a3.06 3.06 0 0 1 4.477-.17c.517.519.815 1.186.875 1.863l-.02-.02z"/><path fill="#C3EF3C" d="M21.77 4.91a3.05 3.05 0 0 0-1.014 2.789c.02.15-.02.289-.13.398l-.02.02a.444.444 0 0 1-.636 0L14.153 2.3a1.007 1.007 0 0 0-1.433 0L9.608 5.417a1.373 1.373 0 0 0 0 1.943l.03.02c.268.27.646.419 1.034.399a3.05 3.05 0 0 1 2.456 1.056a3.07 3.07 0 0 1 0 4.005a3.06 3.06 0 0 1-4.475.17a3.12 3.12 0 0 1-.885-2.362c.03-.389-.12-.777-.398-1.046a1.367 1.367 0 0 0-1.94 0L2.299 12.74a1.01 1.01 0 0 0 0 1.435l5.838 5.848a.446.446 0 0 1 0 .638a.43.43 0 0 1-.398.12a3.06 3.06 0 0 0-2.814.996a3.075 3.075 0 0 0-.01 4.015a3.05 3.05 0 0 0 4.475.16a3.06 3.06 0 0 0 .855-2.64a.46.46 0 0 1 .13-.4l.02-.02a.444.444 0 0 1 .636 0l5.798 5.81a1.007 1.007 0 0 0 1.432 0l3.112-3.12a1.373 1.373 0 0 0 0-1.942l-.02-.02a1.37 1.37 0 0 0-1.034-.399a3.05 3.05 0 0 1-2.456-1.056a3.07 3.07 0 0 1 0-4.005a3.06 3.06 0 0 1 4.475-.17c.646.648.945 1.505.885 2.352c-.02.389.12.767.398 1.046a1.367 1.367 0 0 0 1.94 0l3.142-3.148a1.01 1.01 0 0 0 0-1.435l-5.828-5.838a.446.446 0 0 1 0-.638c.11-.11.259-.15.398-.12a3.05 3.05 0 0 0 2.675-.846a3.063 3.063 0 0 0-.17-4.484c-1.153-.956-2.873-.956-4.007.03"/></g></svg>`
  },
  {
    id: "kmind-icon://builtin/focus/rocket",
    group: "focus",
    name: "rocket",
    label: "Launch",
    catalog: { "groupId": "focus", "groupLabel": "Focus & Goals", "order": 160, "surfaces": ["node-content"] },
    viewBox: "0 0 32 32",
    svg: `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32" width="100%" height="100%" aria-hidden="true" focusable="false"><g fill="none"><path fill="#CA0B4A" d="M29.2 2.95c-.947-.947-2.7-.998-3.818-.425c-.913.314-1.874.667-2.854 1.063l.01.01c-2.575 1.095-6.427 3.04-9.51 5.902c-2.164 2.01-3.404 3.556-4.235 4.965l-5.298 1.95a1 1 0 0 0-.362 1.646l11.138 11.137a1 1 0 0 0 1.645-.362l2.204-5.986c1.608-.958 3.223-2.165 4.908-3.85c2.39-2.39 4.366-6.56 5.513-9.357l.009.008c.4-.99.758-1.961 1.074-2.883c.573-1.118.74-2.654-.424-3.818"/><path fill="#F4F4F4" d="M23.299 4.365c-2.517 1.04-6.478 2.978-9.59 5.868c-2.015 1.87-3.172 3.294-3.94 4.55c-.769 1.255-1.175 2.38-1.663 3.74l-.002.007c-.17.474-.35.977-.559 1.514l4.556 4.556c3.602-1.48 6.74-2.828 10.22-6.307c2.351-2.352 4.339-6.642 5.454-9.421z"/><path fill="#9B9B9B" d="M24.528 11.25a3.25 3.25 0 1 1-6.5 0a3.25 3.25 0 0 1 6.5 0"/><path fill="#83CBFF" d="M23.528 11.25a2.25 2.25 0 1 1-4.5 0a2.25 2.25 0 0 1 4.5 0"/><path fill="#FF8257" d="M2.451 29.61C1.744 28.905 2.028 24 4.528 23c0 0 2.5-1 4.11.6c1.612 1.601.89 3.4.89 3.4c-.707 2.121-3.718 2.965-4.071 2.61c-.195-.194.156-.55 0-.706c-.157-.157-.398.022-1.06.353c-.472.236-1.663.637-1.946.354"/><path fill="#533566" d="M6.088 21.06a1.5 1.5 0 0 1 2.122 0l3.535 3.536a1.5 1.5 0 1 1-2.121 2.122l-3.536-3.536a1.5 1.5 0 0 1 0-2.121"/><path fill="#F92F60" d="M15.535 18.722c.442-1.2-.725-2.368-1.926-1.926l-7.114 2.619a1 1 0 0 0-.362 1.646l5.138 5.137a1 1 0 0 0 1.645-.362z"/></g></svg>`
  },
  {
    id: "kmind-icon://builtin/focus/sparkles",
    group: "focus",
    name: "sparkles",
    label: "Highlight",
    catalog: { "groupId": "focus", "groupLabel": "Focus & Goals", "order": 160, "surfaces": ["node-content"] },
    viewBox: "0 0 32 32",
    svg: `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32" width="100%" height="100%" aria-hidden="true" focusable="false"><path fill="#F9C23C" d="M10.52 7.052a1.17 1.17 0 0 1-.639-.636L8.93 4.257c-.178-.343-.69-.343-.858 0l-.952 2.16a1.28 1.28 0 0 1-.638.635l-1.214.524a.462.462 0 0 0 0 .838l1.214.524c.293.121.523.353.638.636l.952 2.169c.178.343.69.343.858 0l.952-2.17c.126-.282.356-.504.638-.635l1.214-.524a.462.462 0 0 0 0-.838zm15.054 6.503a3.73 3.73 0 0 1-1.922-1.977L20.79 4.81a1.432 1.432 0 0 0-2.58 0l-2.863 6.768a3.8 3.8 0 0 1-1.921 1.977l-3.622 1.64c-1.072.53-1.072 2.08 0 2.61l3.622 1.64a3.74 3.74 0 0 1 1.922 1.977l2.862 6.768a1.432 1.432 0 0 0 2.58 0l2.863-6.768a3.8 3.8 0 0 1 1.921-1.977l3.622-1.64c1.072-.53 1.072-2.08 0-2.61zM8.281 20.33c.16.392.454.696.822.872l1.55.725a.646.646 0 0 1 0 1.146l-1.55.725c-.368.176-.661.49-.822.872l-1.228 2.977a.61.61 0 0 1-1.106 0L4.72 24.67a1.66 1.66 0 0 0-.822-.872l-1.55-.725a.646.646 0 0 1 0-1.146l1.55-.725c.368-.176.661-.49.822-.872l1.228-2.977a.61.61 0 0 1 1.106 0z"/></svg>`
  },
  {
    id: "kmind-icon://builtin/focus/trophy",
    group: "focus",
    name: "trophy",
    label: "Milestone",
    catalog: { "groupId": "focus", "groupLabel": "Focus & Goals", "order": 160, "surfaces": ["node-content"] },
    viewBox: "0 0 32 32",
    svg: `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32" width="100%" height="100%" aria-hidden="true" focusable="false"><g fill="none"><path fill="#D3883E" d="M10.52 7.521a3.435 3.435 0 0 0-4.213-2.369a2 2 0 0 0-.163.046c-2.493.831-2.691 4.214-.455 5.45l4.97 2.75a.866.866 0 1 0 .838-1.516l-4.97-2.75c-.982-.543-.823-1.956.16-2.288l.005-.002l.07-.018c.899-.25 1.834.27 2.093 1.175a.866.866 0 1 0 1.666-.478m11.939.478a1.7 1.7 0 0 1 2.118-1.168l.045.011l.007.002c.981.332 1.14 1.745.158 2.288l-4.97 2.75a.866.866 0 1 0 .84 1.516l4.97-2.75c2.235-1.236 2.037-4.619-.456-5.45a2 2 0 0 0-.164-.046a3.435 3.435 0 0 0-4.213 2.37a.866.866 0 1 0 1.666.477m-5.133 9.511v-4.22h-3.34v4.22c0 .74-.33 1.45-.9 1.92l-1.92 1.6h8.98l-1.92-1.6a2.51 2.51 0 0 1-.9-1.92"/><path fill="#FFB02E" d="M15.658 16.54a6.97 6.97 0 0 1-6.97-6.97V2.71c0-.39.32-.71.71-.71h12.53c.39 0 .71.32.71.71v6.86c0 3.85-3.12 6.97-6.98 6.97"/><path fill="#6D4534" d="M22.792 21.03H8.197c-.77 0-1.423.51-1.571 1.22l-1.614 7.09c-.073.33.19.64.549.64h19.878c.359 0 .622-.31.549-.64l-1.614-7.09c-.158-.71-.812-1.22-1.582-1.22"/><path fill="#FFB02E" d="M18.383 23.96h-5.766a.625.625 0 0 0-.613.64v1.81c0 .35.268.64.613.64h5.766c.335 0 .613-.28.613-.64V24.6c0-.35-.268-.64-.613-.64"/></g></svg>`
  },
  {
    id: "kmind-icon://builtin/keycaps/keycap-0",
    group: "keycaps",
    name: "keycap-0",
    label: "Priority 0",
    catalog: { "groupId": "keycaps", "groupLabel": "Priority Numbers", "order": 180, "surfaces": ["node-content"] },
    viewBox: "0 0 32 32",
    svg: `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32" width="100%" height="100%" aria-hidden="true" focusable="false"><g fill="none"><path fill="#94A3B8" d="M2 6a4 4 0 0 1 4-4h20a4 4 0 0 1 4 4v20a4 4 0 0 1-4 4H6a4 4 0 0 1-4-4z"/><path fill="#fff" d="M10 13.75a6 6 0 0 1 12 0v4.5a6 6 0 0 1-12 0zm6-2.5a2.5 2.5 0 0 0-2.5 2.5v4.5a2.5 2.5 0 0 0 5 0v-4.5a2.5 2.5 0 0 0-2.5-2.5"/></g></svg>`
  },
  {
    id: "kmind-icon://builtin/keycaps/keycap-1",
    group: "keycaps",
    name: "keycap-1",
    label: "Priority 1",
    catalog: { "groupId": "keycaps", "groupLabel": "Priority Numbers", "order": 180, "surfaces": ["node-content"] },
    viewBox: "0 0 32 32",
    svg: `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32" width="100%" height="100%" aria-hidden="true" focusable="false"><g fill="none"><path fill="#60A5FA" d="M2 6a4 4 0 0 1 4-4h20a4 4 0 0 1 4 4v20a4 4 0 0 1-4 4H6a4 4 0 0 1-4-4z"/><path fill="#fff" d="M17.574 7.875c.665.266 1.1.91 1.1 1.625v13a1.75 1.75 0 1 1-3.5 0v-8.625l-.157.165a1.75 1.75 0 1 1-2.534-2.413l3.174-3.334a1.75 1.75 0 0 1 1.917-.418"/></g></svg>`
  },
  {
    id: "kmind-icon://builtin/keycaps/keycap-2",
    group: "keycaps",
    name: "keycap-2",
    label: "Priority 2",
    catalog: { "groupId": "keycaps", "groupLabel": "Priority Numbers", "order": 180, "surfaces": ["node-content"] },
    viewBox: "0 0 32 32",
    svg: `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32" width="100%" height="100%" aria-hidden="true" focusable="false"><g fill="none"><path fill="#38BDF8" d="M2 6a4 4 0 0 1 4-4h20a4 4 0 0 1 4 4v20a4 4 0 0 1-4 4H6a4 4 0 0 1-4-4z"/><path fill="#fff" d="M16.3 11.252c-.31.015-.8.168-1.35.823a1.75 1.75 0 0 1-2.678-2.252c1.077-1.282 2.43-1.996 3.853-2.067c1.4-.07 2.68.493 3.593 1.404c1.905 1.9 2.141 5.144-.302 7.768c-.71.763-1.574 1.665-2.445 2.576c-.4.418-.801.837-1.19 1.246h4.099a1.75 1.75 0 1 1 0 3.5h-7.02c-1.88 0-3.005-2.244-1.66-3.728c.852-.939 2.117-2.261 3.322-3.522c.866-.906 1.702-1.78 2.333-2.457c.666-.716.84-1.343.843-1.784c.001-.457-.18-.85-.452-1.121a1.25 1.25 0 0 0-.946-.386"/></g></svg>`
  },
  {
    id: "kmind-icon://builtin/keycaps/keycap-3",
    group: "keycaps",
    name: "keycap-3",
    label: "Priority 3",
    catalog: { "groupId": "keycaps", "groupLabel": "Priority Numbers", "order": 180, "surfaces": ["node-content"] },
    viewBox: "0 0 32 32",
    svg: `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32" width="100%" height="100%" aria-hidden="true" focusable="false"><g fill="none"><path fill="#22C55E" d="M2 6a4 4 0 0 1 4-4h20a4 4 0 0 1 4 4v20a4 4 0 0 1-4 4H6a4 4 0 0 1-4-4z"/><path fill="#fff" d="M14.291 12.225a1.556 1.556 0 1 1 2.015 2.105a1.75 1.75 0 0 0-.252 3.443l.086.023a1.558 1.558 0 0 1-.446 3.047a1.56 1.56 0 0 1-1.483-1.083a1.75 1.75 0 0 0-3.335 1.061a5.057 5.057 0 1 0 8.737-4.728a5.056 5.056 0 1 0-8.475-5.388a1.75 1.75 0 0 0 3.153 1.52"/></g></svg>`
  },
  {
    id: "kmind-icon://builtin/keycaps/keycap-4",
    group: "keycaps",
    name: "keycap-4",
    label: "Priority 4",
    catalog: { "groupId": "keycaps", "groupLabel": "Priority Numbers", "order": 180, "surfaces": ["node-content"] },
    viewBox: "0 0 32 32",
    svg: `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32" width="100%" height="100%" aria-hidden="true" focusable="false"><g fill="none"><path fill="#84CC16" d="M2 6a4 4 0 0 1 4-4h20a4 4 0 0 1 4 4v20a4 4 0 0 1-4 4H6a4 4 0 0 1-4-4z"/><path fill="#fff" d="M14.613 7.802a1.75 1.75 0 0 1 1.275 2.121l-1.292 5.182h1.9V14a1.75 1.75 0 1 1 3.5 0v1.14a1.75 1.75 0 0 1 0 3.43v3.81a1.75 1.75 0 1 1-3.5 0v-3.775h-4.14a1.75 1.75 0 0 1-1.698-2.173l1.834-7.355a1.75 1.75 0 0 1 2.121-1.275"/></g></svg>`
  },
  {
    id: "kmind-icon://builtin/keycaps/keycap-5",
    group: "keycaps",
    name: "keycap-5",
    label: "Priority 5",
    catalog: { "groupId": "keycaps", "groupLabel": "Priority Numbers", "order": 180, "surfaces": ["node-content"] },
    viewBox: "0 0 32 33",
    svg: `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 33" width="100%" height="100%" aria-hidden="true" focusable="false"><g fill="none"><path fill="#FACC15" d="M2 6.12a4 4 0 0 1 4-4h20a4 4 0 0 1 4 4v20a4 4 0 0 1-4 4H6a4 4 0 0 1-4-4z"/><path fill="#fff" d="M11.078 9.87c0-.966.784-1.75 1.75-1.75h5.438a1.75 1.75 0 0 1 0 3.5h-3.688v1.525h.969a5.61 5.61 0 1 1-4.206 9.321a1.75 1.75 0 0 1 2.624-2.316a2.11 2.11 0 1 0 1.582-3.504h-2.719a1.75 1.75 0 0 1-1.75-1.75z"/></g></svg>`
  },
  {
    id: "kmind-icon://builtin/keycaps/keycap-6",
    group: "keycaps",
    name: "keycap-6",
    label: "Priority 6",
    catalog: { "groupId": "keycaps", "groupLabel": "Priority Numbers", "order": 180, "surfaces": ["node-content"] },
    viewBox: "0 0 32 32",
    svg: `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32" width="100%" height="100%" aria-hidden="true" focusable="false"><g fill="none"><path fill="#F59E0B" d="M2 6a4 4 0 0 1 4-4h20a4 4 0 0 1 4 4v20a4 4 0 0 1-4 4H6a4 4 0 0 1-4-4z"/><path fill="#fff" d="M19.117 10.618a1.75 1.75 0 1 0-2.984-1.83l-4.531 7.391a1.8 1.8 0 0 0-.177.387a5.25 5.25 0 1 0 5.8-2.863zm-4.71 8.226a1.75 1.75 0 1 1 3.5 0a1.75 1.75 0 0 1-3.5 0"/></g></svg>`
  },
  {
    id: "kmind-icon://builtin/keycaps/keycap-7",
    group: "keycaps",
    name: "keycap-7",
    label: "Priority 7",
    catalog: { "groupId": "keycaps", "groupLabel": "Priority Numbers", "order": 180, "surfaces": ["node-content"] },
    viewBox: "0 0 32 32",
    svg: `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32" width="100%" height="100%" aria-hidden="true" focusable="false"><g fill="none"><path fill="#FB923C" d="M2 6a4 4 0 0 1 4-4h20a4 4 0 0 1 4 4v20a4 4 0 0 1-4 4H6a4 4 0 0 1-4-4z"/><path fill="#fff" d="M11.038 9.722c0-.966.784-1.75 1.75-1.75h7.474a1.75 1.75 0 0 1 1.52 2.619l-7.253 12.695a1.75 1.75 0 0 1-3.039-1.736l5.757-10.078h-4.459a1.75 1.75 0 0 1-1.75-1.75"/></g></svg>`
  },
  {
    id: "kmind-icon://builtin/keycaps/keycap-8",
    group: "keycaps",
    name: "keycap-8",
    label: "Priority 8",
    catalog: { "groupId": "keycaps", "groupLabel": "Priority Numbers", "order": 180, "surfaces": ["node-content"] },
    viewBox: "0 0 32 32",
    svg: `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32" width="100%" height="100%" aria-hidden="true" focusable="false"><g fill="none"><path fill="#F97316" d="M2 6a4 4 0 0 1 4-4h20a4 4 0 0 1 4 4v20a4 4 0 0 1-4 4H6a4 4 0 0 1-4-4z"/><path fill="#fff" d="M15.972 7.968a4.516 4.516 0 0 0-3.534 7.329a5.237 5.237 0 1 0 7.091-.03a4.516 4.516 0 0 0-3.557-7.3m-1.266 4.516a1.266 1.266 0 1 1 2.532 0a1.266 1.266 0 0 1-2.532 0m-.443 6.652a1.737 1.737 0 1 1 3.474 0a1.737 1.737 0 0 1-3.474 0"/></g></svg>`
  },
  {
    id: "kmind-icon://builtin/keycaps/keycap-9",
    group: "keycaps",
    name: "keycap-9",
    label: "Priority 9",
    catalog: { "groupId": "keycaps", "groupLabel": "Priority Numbers", "order": 180, "surfaces": ["node-content"] },
    viewBox: "0 0 32 32",
    svg: `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32" width="100%" height="100%" aria-hidden="true" focusable="false"><g fill="none"><path fill="#EF4444" d="M2 6a4 4 0 0 1 4-4h20a4 4 0 0 1 4 4v20a4 4 0 0 1-4 4H6a4 4 0 0 1-4-4z"/><path fill="#fff" d="M20.888 15.481a5.25 5.25 0 1 0-5.8 2.863l-1.892 3.085a1.75 1.75 0 0 0 2.983 1.83l4.532-7.391q.114-.187.177-.387m-2.982-2.278a1.75 1.75 0 1 1-3.5 0a1.75 1.75 0 0 1 3.5 0"/></g></svg>`
  },
  {
    id: "kmind-icon://builtin/keycaps/keycap-asterisk",
    group: "keycaps",
    name: "keycap-asterisk",
    label: "Priority *",
    catalog: { "groupId": "keycaps", "groupLabel": "Priority Numbers", "order": 180, "surfaces": ["node-content"] },
    viewBox: "0 0 32 32",
    svg: `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32" width="100%" height="100%" aria-hidden="true" focusable="false"><g fill="none"><path fill="#A855F7" d="M2 6a4 4 0 0 1 4-4h20a4 4 0 0 1 4 4v20a4 4 0 0 1-4 4H6a4 4 0 0 1-4-4z"/><path fill="#fff" d="M16.022 7.75c.967 0 1.75.784 1.75 1.75v3.456l2.982-1.721a1.75 1.75 0 1 1 1.75 3.03L19.5 16l3.004 1.735a1.75 1.75 0 1 1-1.75 3.03l-2.982-1.721V22.5a1.75 1.75 0 1 1-3.5 0v-3.482l-3.026 1.748a1.75 1.75 0 0 1-1.75-3.031L12.5 16l-3.004-1.734a1.75 1.75 0 0 1 1.75-3.031l3.026 1.747V9.5c0-.966.784-1.75 1.75-1.75"/></g></svg>`
  },
  {
    id: "kmind-icon://builtin/keycaps/keycap-hashtag",
    group: "keycaps",
    name: "keycap-hashtag",
    label: "Priority #",
    catalog: { "groupId": "keycaps", "groupLabel": "Priority Numbers", "order": 180, "surfaces": ["node-content"] },
    viewBox: "0 0 32 32",
    svg: `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32" width="100%" height="100%" aria-hidden="true" focusable="false"><g fill="none"><path fill="#14B8A6" d="M2 6a4 4 0 0 1 4-4h20a4 4 0 0 1 4 4v20a4 4 0 0 1-4 4H6a4 4 0 0 1-4-4z"/><path fill="#fff" d="M12.412 9.404a1.497 1.497 0 1 1 2.989.186l-.134 2.144a.25.25 0 0 0 .25.266h1.498a.25.25 0 0 0 .25-.234l.147-2.362a1.497 1.497 0 1 1 2.989.186l-.134 2.144a.25.25 0 0 0 .25.266h.983a1.5 1.5 0 0 1 0 3h-1.203a.25.25 0 0 0-.25.234l-.093 1.5a.25.25 0 0 0 .25.266H21.5a1.5 1.5 0 0 1 0 3h-1.515a.25.25 0 0 0-.25.234l-.147 2.362a1.497 1.497 0 1 1-2.989-.186l.134-2.144a.25.25 0 0 0-.25-.266h-1.498a.25.25 0 0 0-.25.234l-.147 2.362a1.497 1.497 0 1 1-2.989-.186l.134-2.144a.25.25 0 0 0-.25-.266H10.5a1.5 1.5 0 0 1 0-3h1.203a.25.25 0 0 0 .25-.234l.093-1.5a.25.25 0 0 0-.25-.266H10.5a1.5 1.5 0 0 1 0-3h1.515a.25.25 0 0 0 .25-.234zM16.702 17a.25.25 0 0 0 .25-.234l.094-1.5a.25.25 0 0 0-.25-.266h-1.499a.25.25 0 0 0-.25.234l-.093 1.5a.25.25 0 0 0 .25.266z"/></g></svg>`
  },
  {
    id: "kmind-icon://builtin/knowledge/books",
    group: "knowledge",
    name: "books",
    label: "Reading",
    catalog: { "groupId": "knowledge", "groupLabel": "Knowledge", "order": 130, "surfaces": ["node-content"] },
    viewBox: "0 0 32 32",
    svg: `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32" width="100%" height="100%" aria-hidden="true" focusable="false"><g fill="none"><path fill="#00A6ED" d="M17.045 27.286H30V13a2 2 0 0 0-2-2H17.045z"/><path fill="#D3D3D3" d="M15.682 27.964H30v1.357H15.682z"/><path fill="#0074BA" d="M16.023 11A1.02 1.02 0 0 0 15 12.018v16.625h.682a.68.68 0 0 1 .682-.679h.681V11z"/><path fill="#0074BA" d="M16.023 27.286A1.02 1.02 0 0 0 15 28.304v.678A1.02 1.02 0 0 0 16.023 30h12.954c.446 0 .824-.283.965-.678H16.364a.68.68 0 0 1-.682-.68a.68.68 0 0 1 .682-.678H30v-.678z"/><path fill="#CA0B4A" d="M10.045 23.286H23V9a2 2 0 0 0-2-2H10.045z"/><path fill="#D3D3D3" d="M8.682 23.964H23v1.357H8.682z"/><path fill="#990838" d="M9.023 7A1.02 1.02 0 0 0 8 8.018v16.625h.682a.68.68 0 0 1 .682-.679h.681V7z"/><path fill="#990838" d="M9.023 23.286A1.02 1.02 0 0 0 8 24.304v.678A1.02 1.02 0 0 0 9.023 26h12.954c.446 0 .824-.283.965-.678H9.364a.68.68 0 0 1-.682-.68a.68.68 0 0 1 .682-.678H23v-.678z"/><path fill="#86D72F" d="M4.045 20.286H17V6a2 2 0 0 0-2-2H4.045z"/><path fill="#D3D3D3" d="M2.682 20.964H17v1.357H2.682z"/><path fill="#44911B" d="M3.023 4A1.02 1.02 0 0 0 2 5.018v16.625h.682a.68.68 0 0 1 .682-.679h.681V4z"/><path fill="#008463" d="M3.023 20.286A1.02 1.02 0 0 0 2 21.304v.678A1.02 1.02 0 0 0 3.023 23h12.954c.446 0 .824-.283.965-.678H3.364a.68.68 0 0 1-.682-.68a.68.68 0 0 1 .682-.678H17v-.678z"/></g></svg>`
  },
  {
    id: "kmind-icon://builtin/knowledge/graduation-cap",
    group: "knowledge",
    name: "graduation-cap",
    label: "Learning",
    catalog: { "groupId": "knowledge", "groupLabel": "Knowledge", "order": 130, "surfaces": ["node-content"] },
    viewBox: "0 0 32 32",
    svg: `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32" width="100%" height="100%" aria-hidden="true" focusable="false"><g fill="none"><path fill="#533566" d="M19.3 23.138h-6.64c-3.84 0-6.95-3.11-6.95-6.95v-4.36h20.53v4.36c.01 3.84-3.1 6.95-6.94 6.95"/><path fill="#321B41" d="m17.13 5.278l12.28 6.29c.76.39.76 1.48 0 1.87l-12.28 6.29c-.72.37-1.56.37-2.28 0l-12.28-6.29c-.76-.39-.76-1.48 0-1.87l12.28-6.29a2.48 2.48 0 0 1 2.28 0"/><path fill="#FFB02E" d="M15.15 12.048c.19-.41.68-.57 1.08-.37l6.71 3.44c.27.14.43.41.43.71v6.28a1.83 1.83 0 0 1 .97 2.1v.02c-.01.04-.02.09-.04.13c0 .01-.01.02-.01.03c-.01.04-.03.08-.05.12c0 .01-.01.02-.01.02c-.05.11-.12.22-.19.31c-.01.02-.02.03-.04.05l.47 2.2a1.94 1.94 0 0 1-1.9 2.35a1.94 1.94 0 0 1-1.9-2.35l.47-2.2c-.25-.31-.4-.7-.4-1.13c0-.25.05-.49.14-.7c0-.01.01-.02.02-.03c.01-.03.03-.07.05-.1c.02-.04.04-.08.07-.12c.01-.01.01-.02.02-.03c.18-.28.44-.51.74-.66v-5.8l-6.25-3.2c-.39-.2-.57-.68-.38-1.07"/></g></svg>`
  },
  {
    id: "kmind-icon://builtin/knowledge/light-bulb",
    group: "knowledge",
    name: "light-bulb",
    label: "Idea",
    catalog: { "groupId": "knowledge", "groupLabel": "Knowledge", "order": 130, "surfaces": ["node-content"] },
    viewBox: "0 0 32 32",
    svg: `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32" width="100%" height="100%" aria-hidden="true" focusable="false"><g fill="none"><path fill="#9B9B9B" d="M17.651 22.27h-3.89c-.79 0-1.44.64-1.43 1.43v3.89c0 .79.64 1.43 1.43 1.43h.248a1.94 1.94 0 0 0 3.384 0h.258c.79 0 1.43-.64 1.43-1.43V23.7c0-.79-.64-1.43-1.43-1.43"/><path fill="#FCD53F" d="M18.161 23.13c.24 0 .43-.18.45-.41c.07-.86.44-2.95 2.46-5.19a8.66 8.66 0 0 0 3.29-6.31c.02-.24.03-.4.03-.5v-.1c-.06-4.78-3.93-8.62-8.7-8.62a8.69 8.69 0 0 0-8.69 8.6s-.01.24.03.64c.16 2.54 1.4 4.79 3.29 6.28c2.02 2.25 2.42 4.34 2.49 5.2c.02.23.21.41.45.41z"/><path fill="#FFB02E" d="M15.701 10.7c1.62 0 2.94 1.31 2.96 2.93v.08c0 .03 0 .07-.01.13c-.05.84-.46 1.63-1.12 2.15l-.07.05l-.06.06c-1.1 1.22-1.33 4.32-1.37 6.02h-.65c-.05-1.7-.29-4.8-1.39-6.02l-.06-.06l-.07-.05a2.96 2.96 0 0 1-1.12-2.17c0-.04-.01-.07-.01-.09v-.09c.03-1.62 1.36-2.94 2.97-2.94m0-1a3.96 3.96 0 0 0-2.45 7.07c1.2 1.34 1.14 6.36 1.14 6.36h2.64s-.08-5.02 1.13-6.35c.86-.68 1.43-1.71 1.5-2.88c.01-.11.01-.18.01-.23v-.04a3.97 3.97 0 0 0-3.97-3.93"/><path fill="#D3D3D3" d="M19.167 25.053a.5.5 0 1 0-.172-.986l-6.74 1.18a.5.5 0 1 0 .172.986zm-.05 2.15a.5.5 0 0 0-.172-.985l-6.65 1.17a.5.5 0 1 0 .173.984z"/><path fill="#FFF478" d="M13.791 5.44c-1.11 1.92-.55 4.32 1.25 5.35s4.15.32 5.26-1.6s.55-4.32-1.25-5.35s-4.15-.32-5.26 1.6"/></g></svg>`
  },
  {
    id: "kmind-icon://builtin/knowledge/magnifying-glass-tilted-left",
    group: "knowledge",
    name: "magnifying-glass-tilted-left",
    label: "Explore",
    catalog: { "groupId": "knowledge", "groupLabel": "Knowledge", "order": 130, "surfaces": ["node-content"] },
    viewBox: "0 0 32 32",
    svg: `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32" width="100%" height="100%" aria-hidden="true" focusable="false"><g fill="none"><path fill="#00A6ED" d="M3 13c0 5.523 4.477 10 10 10s10-4.477 10-10S18.523 3 13 3S3 7.477 3 13"/><path fill="#fff" d="M18.348 7.732c.552.957.419 2.068-.299 2.482c-.717.414-1.747-.025-2.299-.982s-.418-2.068.299-2.482c.718-.414 1.747.025 2.3.982"/><path fill="#533566" d="M2 13c0 6.075 4.925 11 11 11c2.295 0 4.426-.703 6.19-1.905a3.75 3.75 0 0 0 1.005 3.483l3.182 3.182a3.75 3.75 0 0 0 5.303-5.303l-3.182-3.182a3.75 3.75 0 0 0-3.454-1.012A10.95 10.95 0 0 0 24 13c0-6.075-4.925-11-11-11S2 6.925 2 13m20 0a9 9 0 1 1-18 0a9 9 0 0 1 18 0"/></g></svg>`
  },
  {
    id: "kmind-icon://builtin/knowledge/microscope",
    group: "knowledge",
    name: "microscope",
    label: "Research",
    catalog: { "groupId": "knowledge", "groupLabel": "Knowledge", "order": 130, "surfaces": ["node-content"] },
    viewBox: "0 0 32 32",
    svg: `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32" width="100%" height="100%" aria-hidden="true" focusable="false"><g fill="none"><path fill="#5092FF" d="M4.718 18.023a1.25 1.25 0 0 1 1.742-.305l12.072 8.476l-1.437 2.047l-12.072-8.476a1.25 1.25 0 0 1-.305-1.742"/><path fill="#636363" d="M18.501 2.803c.33-.443.96-.543 1.41-.223l1.673 1.191c.45.32.548.94.22 1.384L13.11 16.88a2.074 2.074 0 0 1-2.858.453a1.98 1.98 0 0 1-.444-2.804z"/><path fill="#BEBEBE" d="M18.047 3.666c-1.209-.352-2.667.195-3.45 1.251l-2.822 3.807L12 10l-1.398.306l-.203.275a3.95 3.95 0 0 0 .903 5.587c1.823 1.298 4.376.902 5.7-.885l.16-.215L17 13.5h1.324l.164-.221c3.504.651 5.38 3.572 5.475 6.576c.052 1.65-.442 3.276-1.482 4.535c-1.027 1.243-2.67 2.229-5.102 2.459c-.834.079-1.449.847-1.373 1.715s.814 1.509 1.648 1.43c3.129-.297 5.53-1.614 7.126-3.545c1.582-1.915 2.289-4.335 2.215-6.698c-.123-3.895-2.39-7.767-6.49-9.192l.696-.94c.783-1.056.863-2.584.148-3.602z"/><path fill="#9B9B9B" d="M2 29.2A3.2 3.2 0 0 1 5.2 26h21.6a3.2 3.2 0 0 1 3.2 3.2a.8.8 0 0 1-.8.8H2.8a.8.8 0 0 1-.8-.8"/><path fill="#D3D3D3" d="m11.776 8.71l6.558 4.765l-1.175 1.618l-6.559-4.765z"/></g></svg>`
  },
  {
    id: "kmind-icon://builtin/knowledge/open-book",
    group: "knowledge",
    name: "open-book",
    label: "Knowledge",
    catalog: { "groupId": "knowledge", "groupLabel": "Knowledge", "order": 130, "surfaces": ["node-content"] },
    viewBox: "0 0 32 32",
    svg: `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32" width="100%" height="100%" aria-hidden="true" focusable="false"><g fill="none"><path fill="#B4ACBC" fill-rule="evenodd" d="M16 8.05A3.5 3.5 0 0 1 18.5 7h8c.743 0 1.39.404 1.734 1.003c.07.121.096.26.096.4v2.294L29 25.5a2.5 2.5 0 0 1-2.5 2.5h-21A2.5 2.5 0 0 1 3 25.5l.67-14.803V8.403c0-.14.026-.279.096-.4A2 2 0 0 1 5.5 7h8c.98 0 1.865.402 2.5 1.05" clip-rule="evenodd"/><path fill="#0074BA" d="M17.732 30H28.5c.83 0 1.501-.678 1.501-1.505V27.44c0-.827-.67-2.441-1.501-2.441h-25C2.671 25 2 26.614 2 27.441v1.064C2 29.332 2.67 30 3.501 30h10.767a2 2 0 0 0 3.464 0"/><path fill="#00A6ED" fill-rule="evenodd" d="M3.501 10H14v1h4v-1h10.499c.83 0 1.501.668 1.501 1.495v16c0 .827-.67 1.505-1.501 1.505H17.732a2 2 0 0 1-3.464 0H3.5c-.829 0-1.5-.668-1.5-1.495v-16.01C2 10.668 2.67 10 3.501 10M17.5 27.5a1.5 1.5 0 1 1-3 0a1.5 1.5 0 0 1 3 0" clip-rule="evenodd"/><path fill="#B4ACBC" d="M13 8H5.803a1.5 1.5 0 0 0-1.248.668L3 11v14.5A1.5 1.5 0 0 0 4.5 27h23a1.5 1.5 0 0 0 1.5-1.5V11l-1.555-2.332A1.5 1.5 0 0 0 26.197 8H19v3h-6z"/><path fill="#F3EEF8" d="M5.5 8h8a2.5 2.5 0 0 1 2.5 2.5V27l-.447-.894A2 2 0 0 0 13.763 25H5.5a1 1 0 0 1-1-1V9a1 1 0 0 1 1-1m13 0h8a1 1 0 0 1 1 1v15a1 1 0 0 1-1 1h-8.264a2 2 0 0 0-1.736 1.007V9c.456-.607 1.182-1 2-1"/></g></svg>`
  },
  {
    id: "kmind-icon://builtin/pie-progress/pie-0",
    group: "pie-progress",
    name: "pie-0",
    label: "Pie 0%",
    catalog: { "groupId": "pie-progress", "groupLabel": "Pie Progress", "order": 115, "surfaces": ["node-content"] },
    viewBox: "0 0 32 32",
    svg: `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32" width="100%" height="100%" aria-hidden="true" focusable="false"><g fill="none"><circle cx="16" cy="16" r="12" fill="#E5E7EB"/><g fill="#22C55E"></g><circle cx="16" cy="16" r="12" fill="none" stroke="#475569" stroke-width="1.5"/></g></svg>`
  },
  {
    id: "kmind-icon://builtin/pie-progress/pie-100",
    group: "pie-progress",
    name: "pie-100",
    label: "Pie 100%",
    catalog: { "groupId": "pie-progress", "groupLabel": "Pie Progress", "order": 115, "surfaces": ["node-content"] },
    viewBox: "0 0 32 32",
    svg: `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32" width="100%" height="100%" aria-hidden="true" focusable="false"><g fill="none"><circle cx="16" cy="16" r="12" fill="#E5E7EB"/><g fill="#22C55E"><circle cx="16" cy="16" r="12" fill="#22C55E"/></g><circle cx="16" cy="16" r="12" fill="none" stroke="#475569" stroke-width="1.5"/></g></svg>`
  },
  {
    id: "kmind-icon://builtin/pie-progress/pie-25",
    group: "pie-progress",
    name: "pie-25",
    label: "Pie 25%",
    catalog: { "groupId": "pie-progress", "groupLabel": "Pie Progress", "order": 115, "surfaces": ["node-content"] },
    viewBox: "0 0 32 32",
    svg: `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32" width="100%" height="100%" aria-hidden="true" focusable="false"><g fill="none"><circle cx="16" cy="16" r="12" fill="#E5E7EB"/><g fill="#22C55E"><path fill="#22C55E" d="M 16 16 L 16 4 A 12 12 0 0 1 28.000 16.000 Z"/></g><circle cx="16" cy="16" r="12" fill="none" stroke="#475569" stroke-width="1.5"/></g></svg>`
  },
  {
    id: "kmind-icon://builtin/pie-progress/pie-50",
    group: "pie-progress",
    name: "pie-50",
    label: "Pie 50%",
    catalog: { "groupId": "pie-progress", "groupLabel": "Pie Progress", "order": 115, "surfaces": ["node-content"] },
    viewBox: "0 0 32 32",
    svg: `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32" width="100%" height="100%" aria-hidden="true" focusable="false"><g fill="none"><circle cx="16" cy="16" r="12" fill="#E5E7EB"/><g fill="#22C55E"><path fill="#22C55E" d="M 16 16 L 16 4 A 12 12 0 0 1 16.000 28.000 Z"/></g><circle cx="16" cy="16" r="12" fill="none" stroke="#475569" stroke-width="1.5"/></g></svg>`
  },
  {
    id: "kmind-icon://builtin/pie-progress/pie-75",
    group: "pie-progress",
    name: "pie-75",
    label: "Pie 75%",
    catalog: { "groupId": "pie-progress", "groupLabel": "Pie Progress", "order": 115, "surfaces": ["node-content"] },
    viewBox: "0 0 32 32",
    svg: `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32" width="100%" height="100%" aria-hidden="true" focusable="false"><g fill="none"><circle cx="16" cy="16" r="12" fill="#E5E7EB"/><g fill="#22C55E"><path fill="#22C55E" d="M 16 16 L 16 4 A 12 12 0 1 1 4.000 16.000 Z"/></g><circle cx="16" cy="16" r="12" fill="none" stroke="#475569" stroke-width="1.5"/></g></svg>`
  },
  {
    id: "kmind-icon://builtin/planning/calendar",
    group: "planning",
    name: "calendar",
    label: "Calendar",
    catalog: { "groupId": "planning", "groupLabel": "Planning", "order": 120, "surfaces": ["node-content"] },
    viewBox: "0 0 32 32",
    svg: `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32" width="100%" height="100%" aria-hidden="true" focusable="false"><g fill="none"><path fill="#B4ACBC" d="m2 9l13.267-2.843a3.5 3.5 0 0 1 1.466 0L30 9v15.8a5.2 5.2 0 0 1-5.2 5.2H7.2A5.2 5.2 0 0 1 2 24.8z"/><path fill="#F3EEF8" d="m3 8l12.213-2.818a3.5 3.5 0 0 1 1.574 0L29 8v16.5a4.5 4.5 0 0 1-4.5 4.5h-17A4.5 4.5 0 0 1 3 24.5z"/><path fill="#998EA4" d="M8 12a.2.2 0 0 0-.2.2v2.6c0 .11.09.2.2.2h2.8a.2.2 0 0 0 .2-.2v-2.6a.2.2 0 0 0-.2-.2zm0 5.5a.2.2 0 0 0-.2.2v2.6c0 .11.09.2.2.2h2.8a.2.2 0 0 0 .2-.2v-2.6a.2.2 0 0 0-.2-.2zm-.2 5.6c0-.11.09-.2.2-.2h2.8c.11 0 .2.09.2.2v2.6a.2.2 0 0 1-.2.2H8a.2.2 0 0 1-.2-.2zM14.6 12a.2.2 0 0 0-.2.2v2.6c0 .11.09.2.2.2h2.8a.2.2 0 0 0 .2-.2v-2.6a.2.2 0 0 0-.2-.2zm-.2 5.7c0-.11.09-.2.2-.2h2.8c.11 0 .2.09.2.2v2.6a.2.2 0 0 1-.2.2h-2.8a.2.2 0 0 1-.2-.2zm.2 5.2a.2.2 0 0 0-.2.2v2.6c0 .11.09.2.2.2h2.8a.2.2 0 0 0 .2-.2v-2.6a.2.2 0 0 0-.2-.2zM21 12.2c0-.11.09-.2.2-.2H24c.11 0 .2.09.2.2v2.6a.2.2 0 0 1-.2.2h-2.8a.2.2 0 0 1-.2-.2zm.2 10.7a.2.2 0 0 0-.2.2v2.6c0 .11.09.2.2.2H24a.2.2 0 0 0 .2-.2v-2.6a.2.2 0 0 0-.2-.2z"/><path fill="#0084CE" d="M7.2 2A5.2 5.2 0 0 0 2 7.2V9h28V7.2A5.2 5.2 0 0 0 24.8 2zm14 15.5a.2.2 0 0 0-.2.2v2.6c0 .11.09.2.2.2H24a.2.2 0 0 0 .2-.2v-2.6a.2.2 0 0 0-.2-.2z"/></g></svg>`
  },
  {
    id: "kmind-icon://builtin/planning/clipboard",
    group: "planning",
    name: "clipboard",
    label: "Checklist",
    catalog: { "groupId": "planning", "groupLabel": "Planning", "order": 120, "surfaces": ["node-content"] },
    viewBox: "0 0 32 32",
    svg: `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32" width="100%" height="100%" aria-hidden="true" focusable="false"><g fill="none"><path fill="#E19747" d="M5 4.5A1.5 1.5 0 0 1 6.5 3h19A1.5 1.5 0 0 1 27 4.5v24a1.5 1.5 0 0 1-1.5 1.5h-19A1.5 1.5 0 0 1 5 28.5z"/><path fill="#F3EEF8" d="M25 6a1 1 0 0 0-1-1H8a1 1 0 0 0-1 1v21a1 1 0 0 0 1 1h10.586c.147 0 .29-.032.421-.093l.321-.783l.632-4.086l4.457-.783l.49-.247a1 1 0 0 0 .093-.422z"/><path fill="#CDC4D6" d="M24.91 22H20a1 1 0 0 0-1 1v4.91a1 1 0 0 0 .293-.203l5.414-5.414A1 1 0 0 0 24.91 22"/><path fill="#9B9B9B" d="M18 4a2 2 0 1 0-4 0h-1a2 2 0 0 0-2 2v1.5a.5.5 0 0 0 .5.5h9a.5.5 0 0 0 .5-.5V6a2 2 0 0 0-2-2zm-1 0a1 1 0 1 1-2 0a1 1 0 0 1 2 0m-8 8.5a.5.5 0 0 1 .5-.5h13a.5.5 0 0 1 0 1h-13a.5.5 0 0 1-.5-.5m0 3a.5.5 0 0 1 .5-.5h13a.5.5 0 0 1 0 1h-13a.5.5 0 0 1-.5-.5m.5 2.5a.5.5 0 0 0 0 1h13a.5.5 0 0 0 0-1zM9 21.5a.5.5 0 0 1 .5-.5h8a.5.5 0 0 1 0 1h-8a.5.5 0 0 1-.5-.5"/></g></svg>`
  },
  {
    id: "kmind-icon://builtin/planning/memo",
    group: "planning",
    name: "memo",
    label: "Memo",
    catalog: { "groupId": "planning", "groupLabel": "Planning", "order": 120, "surfaces": ["node-content"] },
    viewBox: "0 0 32 32",
    svg: `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32" width="100%" height="100%" aria-hidden="true" focusable="false"><g fill="none"><path fill="#B4ACBC" d="M20.343 2.293A1 1 0 0 0 19.636 2H7a2 2 0 0 0-2 2v24a2 2 0 0 0 2 2h18a2 2 0 0 0 2-2V9.364a1 1 0 0 0-.293-.707z"/><path fill="#F3EEF8" d="M19.682 3H7a1 1 0 0 0-1 1v24a1 1 0 0 0 1 1h18a1 1 0 0 0 1-1V9.453z"/><path fill="#998EA4" d="M9.5 12h13a.5.5 0 0 1 0 1h-13a.5.5 0 0 1 0-1m0 3a.5.5 0 0 0 0 1h13a.5.5 0 0 0 0-1zM9 18.5a.5.5 0 0 1 .5-.5h13a.5.5 0 0 1 0 1h-13a.5.5 0 0 1-.5-.5m.5 2.5a.5.5 0 0 0 0 1h8a.5.5 0 0 0 0-1z"/><path fill="#CDC4D6" d="M26 9.453h-4.61a1.707 1.707 0 0 1-1.708-1.707V3z"/><path fill="#FF822D" d="m26.766 20.172l-1.08-3.231l-2.796-2.006l-10.607 7.849l1.148 3.156l2.727 2.082z"/><path fill="#FFCE7C" d="m11.106 26.655l.171.893l.836.468l4.039-.006l-3.86-5.216z"/><path fill="#402A32" d="m10.687 28.018l.418-1.363l1.007 1.36z"/><path fill="#F92F60" d="M26.52 12.249a2 2 0 0 1 2.798.418l1.496 2.022a2 2 0 0 1-.418 2.797l-2.058 1.524l-2.805-2.069l-1.071-3.17z"/><path fill="#D3D3D3" d="m24.462 13.772l3.876 5.238l-1.572 1.162l-3.875-5.237z"/></g></svg>`
  },
  {
    id: "kmind-icon://builtin/planning/pencil",
    group: "planning",
    name: "pencil",
    label: "Draft",
    catalog: { "groupId": "planning", "groupLabel": "Planning", "order": 120, "surfaces": ["node-content"] },
    viewBox: "0 0 32 32",
    svg: `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32" width="100%" height="100%" aria-hidden="true" focusable="false"><g fill="none"><path fill="#FF822D" d="m16.635 7.585l4.51 2.535l2.561 4.537L9.37 28.993l-4.862-2.57l-2.21-4.5z"/><path fill="#FFCE7C" d="m1.39 28.065l.582 1.312l1.255.525l6.13-.925l-7.042-7.042z"/><path fill="#402A32" d="m1.063 30.229l.326-2.164l1.838 1.837z"/><path fill="#F92F60" d="M22.276 1.944a2 2 0 0 1 2.829 0l4.242 4.243a2 2 0 0 1 0 2.828l-3.535 3.536l-4.527-2.264L18.74 5.48z"/><path fill="#D3D3D3" d="m18.74 5.48l7.072 7.071l-2.122 2.121l-7.07-7.07z"/></g></svg>`
  },
  {
    id: "kmind-icon://builtin/planning/pushpin",
    group: "planning",
    name: "pushpin",
    label: "Pinned",
    catalog: { "groupId": "planning", "groupLabel": "Planning", "order": 120, "surfaces": ["node-content"] },
    viewBox: "0 0 32 32",
    svg: `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32" width="100%" height="100%" aria-hidden="true" focusable="false"><g fill="none"><path fill="#D3D3D3" d="M2.383 29.495c-.51-.51-.51-1.33 0-1.84l8.96-8.96l1.84 1.84l-8.96 8.96c-.51.51-1.33.51-1.84 0"/><path fill="#CA0B4A" d="m20.033 19.174l4.603-4.603L23 8.5l-5.796-1.36l-4.603 4.602L14 17.5z"/><path fill="#F8312F" d="m17.183 7.125l7.47 7.46a2.607 2.607 0 0 0 3.69 0l1.11-1.11c.42-.42.42-1.1 0-1.52l-9.64-9.64c-.42-.42-1.1-.42-1.52 0l-1.11 1.11a2.62 2.62 0 0 0 0 3.7m-11.1 7.44l11.12 11.12c.52.52 1.37.52 1.89 0l.91-.91a3.983 3.983 0 0 0 0-5.64l-7.37-7.37a3.983 3.983 0 0 0-5.64 0l-.91.91a1.34 1.34 0 0 0 0 1.89"/></g></svg>`
  },
  {
    id: "kmind-icon://builtin/planning/spiral-calendar",
    group: "planning",
    name: "spiral-calendar",
    label: "Plan",
    catalog: { "groupId": "planning", "groupLabel": "Planning", "order": 120, "surfaces": ["node-content"] },
    viewBox: "0 0 32 32",
    svg: `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32" width="100%" height="100%" aria-hidden="true" focusable="false"><g fill="none"><path fill="#B4ACBC" d="m2 9l13.267-2.843a3.5 3.5 0 0 1 1.466 0L30 9v15.8a5.2 5.2 0 0 1-5.2 5.2H7.2A5.2 5.2 0 0 1 2 24.8z"/><path fill="#F3EEF8" d="M3 10.905V24.5A4.5 4.5 0 0 0 7.5 29h16l5.5-5.667V10.905L16 9z"/><path fill="#998EA4" d="M8.2 13a.2.2 0 0 0-.2.2v2.6c0 .11.09.2.2.2h2.6a.2.2 0 0 0 .2-.2v-2.6a.2.2 0 0 0-.2-.2zm6.5 0a.2.2 0 0 0-.2.2v2.6c0 .11.09.2.2.2h2.6a.2.2 0 0 0 .2-.2v-2.6a.2.2 0 0 0-.2-.2zm6.3.2c0-.11.09-.2.2-.2h2.6c.11 0 .2.09.2.2v2.6a.2.2 0 0 1-.2.2h-2.6a.2.2 0 0 1-.2-.2zM8.2 18a.2.2 0 0 0-.2.2v2.6c0 .11.09.2.2.2h2.6a.2.2 0 0 0 .2-.2v-2.6a.2.2 0 0 0-.2-.2zm6.3.2c0-.11.09-.2.2-.2h2.6c.11 0 .2.09.2.2v2.6a.2.2 0 0 1-.2.2h-2.6a.2.2 0 0 1-.2-.2zM8.2 23a.2.2 0 0 0-.2.2v2.6c0 .11.09.2.2.2h2.6a.2.2 0 0 0 .2-.2v-2.6a.2.2 0 0 0-.2-.2zm6.3.2c0-.11.09-.2.2-.2h2.6c.11 0 .2.09.2.2v2.6a.2.2 0 0 1-.2.2h-2.6a.2.2 0 0 1-.2-.2zm6.7-.2a.2.2 0 0 0-.2.2v2.6c0 .11.09.2.2.2h2.6a.2.2 0 0 0 .2-.2v-2.6a.2.2 0 0 0-.2-.2zm8.81 3.24V23l-4.51 2.5l-2.49 4.5h3.24c2.08 0 3.76-1.69 3.76-3.76"/><path fill="#E1D8EC" d="M23.01 26.76V30l7-7h-3.24c-2.07 0-3.76 1.69-3.76 3.76"/><path fill="#0084CE" d="M30 8.785V11H2V8.785C2 6.691 3.69 4.99 5.759 5h19.277l.728-.57l.772.582C28.468 5.162 30 6.792 30 8.785M21.2 18a.2.2 0 0 0-.2.2v2.6c0 .11.09.2.2.2h2.6a.2.2 0 0 0 .2-.2v-2.6a.2.2 0 0 0-.2-.2z"/><path fill="#CDC4D6" d="M11.52 5a1.77 1.77 0 0 0 1.11 1.92c.328.128.62.403.62.754c0 .477-.395.875-.855.748a3.27 3.27 0 0 1-2.381-3.456A1.77 1.77 0 1 0 7.63 6.92c.328.127.62.402.62.753c0 .477-.395.875-.855.748A3.271 3.271 0 0 1 8.27 2c1.003 0 1.9.451 2.5 1.162A3.26 3.26 0 0 1 13.27 2c1.003 0 1.9.451 2.5 1.162A3.26 3.26 0 0 1 18.27 2c1.003 0 1.9.451 2.5 1.162A3.27 3.27 0 0 1 26.529 5h-1.51a1.77 1.77 0 0 0-3.493-.034l.003.034h-.009a1.77 1.77 0 0 0 1.11 1.92c.328.128.62.403.62.754c0 .477-.395.875-.855.748a3.27 3.27 0 0 1-2.381-3.456a1.77 1.77 0 0 0-3.488 0l.003.034h-.009a1.77 1.77 0 0 0 1.11 1.92c.328.128.62.403.62.754c0 .477-.395.875-.855.748a3.27 3.27 0 0 1-2.381-3.456a1.77 1.77 0 0 0-3.488 0l.003.034z"/></g></svg>`
  },
  {
    id: "kmind-icon://builtin/progress/alarm-clock",
    group: "progress",
    name: "alarm-clock",
    label: "Deadline",
    catalog: { "groupId": "progress", "groupLabel": "Progress", "order": 110, "surfaces": ["node-content"] },
    viewBox: "0 0 32 32",
    svg: `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32" width="100%" height="100%" aria-hidden="true" focusable="false"><g fill="none"><path fill="#D3D3D3" d="M23.207 24.58C21 25.5 19.05 26 16.5 26c-2.788 0-4.5-.5-7.203-1.86l-2.586 2.237C5.317 27.588 6.11 30 7.905 30H24.09c1.796 0 2.599-2.412 1.194-3.623z"/><path fill="#F8312F" d="M16.5 27C22.299 27 27 22.299 27 16.5S22.299 6 16.5 6S6 10.701 6 16.5S10.701 27 16.5 27"/><path fill="#fff" d="M16.5 24a7.5 7.5 0 1 0 0-15a7.5 7.5 0 0 0 0 15"/><path fill="#F9C23C" d="M4.273 9.228c-.735-2.284.039-4.883 2.033-6.294s4.588-1.178 6.32.396c.542.497.484 1.4-.106 1.817l-6.601 4.66c-.6.416-1.414.132-1.646-.579m24.454 0c.735-2.284-.039-4.883-2.033-6.294s-4.588-1.178-6.32.396c-.542.497-.484 1.4.106 1.817l6.601 4.66c.6.416 1.414.132 1.646-.579"/><path fill="#F8312F" d="M15.168 16.445a1 1 0 0 1 1.387-.277l3 2a1 1 0 1 1-1.11 1.664l-3-2a1 1 0 0 1-.277-1.387"/><path fill="#212121" d="M16 11a1 1 0 0 1 1 1v5a1 1 0 1 1-2 0v-5a1 1 0 0 1 1-1"/></g></svg>`
  },
  {
    id: "kmind-icon://builtin/progress/check-mark-button",
    group: "progress",
    name: "check-mark-button",
    label: "Done",
    catalog: { "groupId": "progress", "groupLabel": "Progress", "order": 110, "surfaces": ["node-content"] },
    viewBox: "0 0 32 32",
    svg: `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32" width="100%" height="100%" aria-hidden="true" focusable="false"><g fill="none"><path fill="#00D26A" d="M2 6a4 4 0 0 1 4-4h20a4 4 0 0 1 4 4v20a4 4 0 0 1-4 4H6a4 4 0 0 1-4-4z"/><path fill="#F4F4F4" d="M13.242 23c-.383 0-.766-.143-1.059-.43l-5.744-5.642a1.453 1.453 0 0 1 0-2.08a1.517 1.517 0 0 1 2.118 0l4.685 4.601L23.443 9.431a1.517 1.517 0 0 1 2.118 0a1.45 1.45 0 0 1 0 2.08l-11.26 11.058a1.5 1.5 0 0 1-1.059.431"/></g></svg>`
  },
  {
    id: "kmind-icon://builtin/progress/cross-mark-button",
    group: "progress",
    name: "cross-mark-button",
    label: "Blocked",
    catalog: { "groupId": "progress", "groupLabel": "Progress", "order": 110, "surfaces": ["node-content"] },
    viewBox: "0 0 32 32",
    svg: `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32" width="100%" height="100%" aria-hidden="true" focusable="false"><g fill="none"><path fill="#00D26A" d="M2 6a4 4 0 0 1 4-4h20a4 4 0 0 1 4 4v20a4 4 0 0 1-4 4H6a4 4 0 0 1-4-4z"/><path fill="#fff" d="M21.564 8.314a1.5 1.5 0 0 1 2.122 2.122L18.12 16l5.565 5.564a1.5 1.5 0 0 1-2.122 2.122L16 18.12l-5.564 5.565a1.5 1.5 0 0 1-2.122-2.122L13.88 16l-5.565-5.564a1.5 1.5 0 0 1 2.122-2.122L16 13.88z"/></g></svg>`
  },
  {
    id: "kmind-icon://builtin/progress/hourglass-done",
    group: "progress",
    name: "hourglass-done",
    label: "Complete",
    catalog: { "groupId": "progress", "groupLabel": "Progress", "order": 110, "surfaces": ["node-content"] },
    viewBox: "0 0 32 32",
    svg: `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32" width="100%" height="100%" aria-hidden="true" focusable="false"><g fill="none"><path fill="#83CBFF" d="M25 6.4V3.9l-9-.4l-9 .4v2.5c0 4 2.8 7.3 6.5 8.2c.3.1.5.4.5.7v1.2c0 .3-.2.6-.5.6C9.8 18 7 21.3 7 25.3V28l9 1l9-1v-2.7c0-4-2.8-7.3-6.5-8.2c-.3-.1-.5-.3-.5-.6v-1.2c0-.3.2-.6.5-.6c3.7-1 6.5-4.3 6.5-8.3"/><path fill="#9B9B9B" d="M7 4h18c.6 0 1-.4 1-1s-.4-1-1-1H7c-.6 0-1 .4-1 1s.4 1 1 1m0 26h18c.6 0 1-.4 1-1s-.4-1-1-1H7c-.6 0-1 .4-1 1s.4 1 1 1"/><path fill="#FFB02E" d="M17 19.4v-4.3c0-.7.5-1.2 1.1-1.4c1.7-.4 3.2-1.4 4.3-2.7c.7-.8.1-2-.9-2h-11c-1 0-1.6 1.2-.9 2c1.1 1.3 2.6 2.2 4.3 2.7c.7.2 1.1.7 1.1 1.4V19c0 .7-.3 1-.6 1.1c-3.7.7-6.4 3.5-6.4 6.8V28h16v-1.1c0-3.3-2.7-6.1-6.4-6.8c-.3 0-.6-.3-.6-.7"/><path fill="#fff" d="M21.5 5.8c0-.5.4-.9.9-.9c.6.1 1 .5.9.9c-.1 1.6-.5 3-1.3 4.2c-.8 1.4-2 2.4-3.4 2.9c-.5.2-1 0-1.2-.5s0-1 .5-1.2c2.4-.9 3.4-3.5 3.6-5.4m0 20.1c0 .5.4.9.9.9c.6 0 1-.5.9-.9c-.1-1.6-.5-3-1.3-4.2c-.8-1.4-2-2.4-3.4-2.9c-.5-.2-1 0-1.2.5s0 1 .5 1.2c2.4.9 3.4 3.5 3.6 5.4"/></g></svg>`
  },
  {
    id: "kmind-icon://builtin/progress/hourglass-not-done",
    group: "progress",
    name: "hourglass-not-done",
    label: "Waiting",
    catalog: { "groupId": "progress", "groupLabel": "Progress", "order": 110, "surfaces": ["node-content"] },
    viewBox: "0 0 32 32",
    svg: `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32" width="100%" height="100%" aria-hidden="true" focusable="false"><g fill="none"><path fill="#83CBFF" d="m25 4l-9-1l-9 1v3.5c.19 2.484 1.823 6.52 7 7.348v2.304c-5.177.829-6.81 4.864-7 7.348V28l9 1l9-1v-3.5c-.19-2.484-1.823-6.52-7-7.348v-2.304c5.177-.829 6.81-4.864 7-7.348z"/><path fill="#FFB02E" d="M17 22.2v-7.4c0-.5.3-.9.8-1c3.2-.7 5.6-3.3 6.1-6.6c.1-.6-.4-1.2-1-1.2H9.1c-.6 0-1.1.6-1 1.2c.5 3.3 2.9 5.9 6.1 6.6c.5.1.8.5.8 1v7.4c0 .5-.3.9-.8 1c-1.9.4-3.5 1.5-4.6 3c-.6.8 0 1.8.9 1.8h11c.9 0 1.5-1 .9-1.7c-1.1-1.5-2.8-2.6-4.6-3c-.5-.2-.8-.6-.8-1.1"/><path fill="#D3D3D3" d="M7 2a1 1 0 0 0 0 2h18a1 1 0 1 0 0-2zm0 26a1 1 0 1 0 0 2h18a1 1 0 1 0 0-2z"/><path fill="#fff" d="M22.007 6.117c.14 1.193-.021 2.147-.4 2.86c-.37.696-.99 1.246-1.939 1.58a1 1 0 1 0 .664 1.886c1.376-.484 2.414-1.347 3.041-2.528c.618-1.164.794-2.551.62-4.032a1 1 0 1 0-1.986.234m-3.136 12.954a1 1 0 0 0-.742 1.857c1.151.46 2.117 1.079 2.79 1.887C21.58 23.605 22 24.628 22 26a1 1 0 1 0 2 0c0-1.828-.578-3.306-1.544-4.465c-.952-1.142-2.236-1.924-3.585-2.464"/></g></svg>`
  },
  {
    id: "kmind-icon://builtin/progress/warning",
    group: "progress",
    name: "warning",
    label: "Warning",
    catalog: { "groupId": "progress", "groupLabel": "Progress", "order": 110, "surfaces": ["node-content"] },
    viewBox: "0 0 32 32",
    svg: `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32" width="100%" height="100%" aria-hidden="true" focusable="false"><g fill="none"><path fill="#FFB02E" d="m14.839 5.668l-12.66 21.93c-.51.89.13 2.01 1.16 2.01h25.32c1.03 0 1.67-1.11 1.16-2.01l-12.66-21.93c-.52-.89-1.8-.89-2.32 0"/><path fill="#000" d="M14.599 21.498a1.4 1.4 0 1 0 2.8-.01v-9.16c0-.77-.62-1.4-1.4-1.4c-.77 0-1.4.62-1.4 1.4zm2.8 3.98a1.4 1.4 0 1 1-2.8 0a1.4 1.4 0 0 1 2.8 0"/></g></svg>`
  },
  {
    id: "kmind-icon://builtin/ui/back",
    group: "ui",
    name: "back",
    label: "Back",
    catalog: { "groupId": "ui", "groupLabel": "UI", "order": 300, "surfaces": ["external-link", "host-ui", "editor-ui"] },
    viewBox: "0 0 24 24",
    svg: `<svg viewBox="0 0 24 24" aria-hidden="true" focusable="false" width="100%" height="100%"><path d="M15 6l-6 6 6 6" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>`
  },
  {
    id: "kmind-icon://builtin/ui/backlinks",
    group: "ui",
    name: "backlinks",
    label: "Backlinks",
    catalog: { "groupId": "ui", "groupLabel": "UI", "order": 300, "surfaces": ["external-link", "host-ui", "editor-ui"] },
    viewBox: "0 0 24 24",
    svg: `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="100%" height="100%" aria-hidden="true" focusable="false"><path fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="m4.929 12.707l7.778-7.778m0 0v4.95m0-4.95h-4.95m11.314 6.364l-7.778 7.778m0 0h4.95m-4.95 0v-4.95"/></svg>`
  },
  {
    id: "kmind-icon://builtin/ui/brush",
    group: "ui",
    name: "brush",
    label: "Brush",
    catalog: { "groupId": "ui", "groupLabel": "UI", "order": 300, "surfaces": ["external-link", "host-ui", "editor-ui"] },
    viewBox: "0 0 24 24",
    svg: `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="100%" height="100%" aria-hidden="true" focusable="false"><path fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="1.2" d="M6 12c-.87.739-4.053 2.566-4 3.901c.015.365.32.67.931 1.281l.972.972M12 18c-.739.87-2.566 4.053-3.901 4c-.365-.015-.67-.32-1.281-.931l-.972-.972m-1.943-1.943l2.392-2.392m-2.392 2.392l1.943 1.943m0 0l1.196-1.196m6.897-.42c-.32.343-.479.515-.694.519s-.386-.168-.73-.512l-7.003-7.003c-.344-.344-.516-.516-.512-.73c.004-.216.176-.375.519-.694c.232-.216.42-.368.624-.494c1.765-1.088 4.006-.058 5.79-1.068c2.057-1.164 3.862-3.313 5.566-5.24c.728-.823 1.093-1.235 1.607-1.258c.926-.043 2.935 1.972 2.893 2.894c-.023.514-.435.878-1.26 1.607c-1.925 1.703-4.074 3.508-5.238 5.564c-1.01 1.785.02 4.026-1.069 5.791a4 4 0 0 1-.493.624"/></svg>`
  },
  {
    id: "kmind-icon://builtin/ui/close",
    group: "ui",
    name: "close",
    label: "Close",
    catalog: { "groupId": "ui", "groupLabel": "UI", "order": 300, "surfaces": ["external-link", "host-ui", "editor-ui"] },
    viewBox: "0 0 24 24",
    svg: `<svg viewBox="0 0 24 24" aria-hidden="true" focusable="false" width="100%" height="100%"><path d="M18 6L6 18" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"/><path d="M6 6l12 12" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"/></svg>`
  },
  {
    id: "kmind-icon://builtin/ui/comments",
    group: "ui",
    name: "comments",
    label: "Comments",
    catalog: { "groupId": "ui", "groupLabel": "UI", "order": 300, "surfaces": ["external-link", "host-ui", "editor-ui"] },
    viewBox: "0 0 24 24",
    svg: `<svg viewBox="0 0 24 24" aria-hidden="true" focusable="false" width="100%" height="100%"><path d="M4 5h16a2 2 0 0 1 2 2v9a2 2 0 0 1-2 2H9l-5 3v-3H4a2 2 0 0 1-2-2V7a2 2 0 0 1 2-2z" fill="none" stroke="currentColor" stroke-width="2" stroke-linejoin="round"/></svg>`
  },
  {
    id: "kmind-icon://builtin/ui/delete",
    group: "ui",
    name: "delete",
    label: "Delete",
    catalog: { "groupId": "ui", "groupLabel": "UI", "order": 300, "surfaces": ["external-link", "host-ui", "editor-ui"] },
    viewBox: "0 0 24 24",
    svg: `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="100%" height="100%" aria-hidden="true" focusable="false"><path fill="currentColor" d="M7.616 20q-.667 0-1.141-.475T6 18.386V6h-.5q-.213 0-.356-.144T5 5.499t.144-.356T5.5 5H9q0-.31.23-.54t.54-.23h4.46q.31 0 .54.23T15 5h3.5q.213 0 .356.144t.144.357t-.144.356T18.5 6H18v12.385q0 .666-.475 1.14t-1.14.475zM17 6H7v12.385q0 .269.173.442t.443.173h8.769q.269 0 .442-.173t.173-.442zm-6.692 11q.213 0 .357-.144t.143-.356v-8q0-.213-.144-.356T10.307 8t-.356.144t-.143.356v8q0 .213.144.356q.144.144.356.144m3.385 0q.213 0 .356-.144t.143-.356v-8q0-.213-.144-.356Q13.904 8 13.692 8q-.213 0-.357.144t-.143.356v8q0 .213.144.356t.357.144M7 6v13z"/></svg>`
  },
  {
    id: "kmind-icon://builtin/ui/drag",
    group: "ui",
    name: "drag",
    label: "Drag",
    catalog: { "groupId": "ui", "groupLabel": "UI", "order": 300, "surfaces": ["external-link", "host-ui", "editor-ui"] },
    viewBox: "0 0 24 24",
    svg: `<svg viewBox="0 0 24 24" aria-hidden="true" focusable="false" width="100%" height="100%"><path d="M9 7h.01M9 12h.01M9 17h.01M15 7h.01M15 12h.01M15 17h.01" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" /></svg>`
  },
  {
    id: "kmind-icon://builtin/ui/enter-submap",
    group: "ui",
    name: "enter-submap",
    label: "Enter SubMap",
    catalog: { "groupId": "ui", "groupLabel": "UI", "order": 300, "surfaces": ["external-link", "host-ui", "editor-ui"] },
    viewBox: "0 0 24 24",
    svg: `<svg viewBox="0 0 24 24" aria-hidden="true" focusable="false" width="100%" height="100%"><path d="M9 6l6 6-6 6" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>`
  },
  {
    id: "kmind-icon://builtin/ui/export",
    group: "ui",
    name: "export",
    label: "Export",
    catalog: { "groupId": "ui", "groupLabel": "UI", "order": 300, "surfaces": ["external-link", "host-ui", "editor-ui"] },
    viewBox: "0 0 24 24",
    svg: `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="100%" height="100%" aria-hidden="true" focusable="false"><path fill="currentColor" d="M8.71 7.71L11 5.41V15a1 1 0 0 0 2 0V5.41l2.29 2.3a1 1 0 0 0 1.42 0a1 1 0 0 0 0-1.42l-4-4a1 1 0 0 0-.33-.21a1 1 0 0 0-.76 0a1 1 0 0 0-.33.21l-4 4a1 1 0 1 0 1.42 1.42M21 14a1 1 0 0 0-1 1v4a1 1 0 0 1-1 1H5a1 1 0 0 1-1-1v-4a1 1 0 0 0-2 0v4a3 3 0 0 0 3 3h14a3 3 0 0 0 3-3v-4a1 1 0 0 0-1-1"/></svg>`
  },
  {
    id: "kmind-icon://builtin/ui/fit",
    group: "ui",
    name: "fit",
    label: "Fit View",
    catalog: { "groupId": "ui", "groupLabel": "UI", "order": 300, "surfaces": ["external-link", "host-ui", "editor-ui"] },
    viewBox: "0 0 24 24",
    svg: `<svg viewBox="0 0 24 24" aria-hidden="true" focusable="false" width="100%" height="100%"><path d="M9 4H4v5" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/><path d="M15 4h5v5" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/><path d="M4 15v5h5" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/><path d="M15 20h5v-5" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>`
  },
  {
    id: "kmind-icon://builtin/ui/help",
    group: "ui",
    name: "help",
    label: "About",
    catalog: { "groupId": "ui", "groupLabel": "UI", "order": 300, "surfaces": ["external-link", "host-ui", "editor-ui"] },
    viewBox: "0 0 24 24",
    svg: `<svg viewBox="0 0 24 24" aria-hidden="true" focusable="false" width="100%" height="100%"><circle cx="12" cy="12" r="9" fill="none" stroke="currentColor" stroke-width="2"/><path d="M9.6 9.2a2.4 2.4 0 1 1 4.6 1c-.4.7-.8 1-1.6 1.6-.9.7-1.4 1.3-1.4 2.4" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/><circle cx="12" cy="17.2" r="1.2" fill="currentColor"/></svg>`
  },
  {
    id: "kmind-icon://builtin/ui/history",
    group: "ui",
    name: "history",
    label: "History",
    catalog: { "groupId": "ui", "groupLabel": "UI", "order": 300, "surfaces": ["external-link", "host-ui", "editor-ui"] },
    viewBox: "0 0 24 24",
    svg: `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="100%" height="100%" aria-hidden="true" focusable="false"><path fill="currentColor" d="M13 3a9 9 0 1 0 8.94 10h-2.02a7 7 0 1 1-6.92-8v3l4-4l-4-4v3ZM12 8v5l4.28 2.54l.72-1.21l-3.5-2.08V8H12Z"/></svg>`
  },
  {
    id: "kmind-icon://builtin/ui/icons",
    group: "ui",
    name: "icons",
    label: "Icons",
    catalog: { "groupId": "ui", "groupLabel": "UI", "order": 300, "surfaces": ["external-link", "host-ui", "editor-ui"] },
    viewBox: "0 0 24 24",
    svg: `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="100%" height="100%" aria-hidden="true" focusable="false"><g fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="1.2"><path d="M9 15c.85.63 1.885 1 3 1s2.15-.37 3-1m-5.5-4.5V10m5 .5V10"/><path d="M21 12a9 9 0 1 1-18 0a9 9 0 0 1 18 0"/></g></svg>`
  },
  {
    id: "kmind-icon://builtin/ui/image",
    group: "ui",
    name: "image",
    label: "Image",
    catalog: { "groupId": "ui", "groupLabel": "UI", "order": 300, "surfaces": ["external-link", "host-ui", "editor-ui"] },
    viewBox: "0 0 24 24",
    svg: `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="100%" height="100%" aria-hidden="true" focusable="false"><path fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M6.5 4.5h11A3 3 0 0 1 20.5 7.5v9a3 3 0 0 1-3 3h-11a3 3 0 0 1-3-3v-9a3 3 0 0 1 3-3Z"/><path fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M6.5 15.5l3-3 3 3 3-3 2 2"/><path fill="none" stroke="currentColor" stroke-width="1.5" d="M9 9.25a1.25 1.25 0 1 0 2.5 0a1.25 1.25 0 0 0-2.5 0Z"/></svg>`
  },
  {
    id: "kmind-icon://builtin/ui/import",
    group: "ui",
    name: "import",
    label: "Import",
    catalog: { "groupId": "ui", "groupLabel": "UI", "order": 300, "surfaces": ["external-link", "host-ui", "editor-ui"] },
    viewBox: "0 0 24 24",
    svg: `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="100%" height="100%" aria-hidden="true" focusable="false"><path fill="currentColor" d="M21 14a1 1 0 0 0-1 1v4a1 1 0 0 1-1 1H5a1 1 0 0 1-1-1v-4a1 1 0 0 0-2 0v4a3 3 0 0 0 3 3h14a3 3 0 0 0 3-3v-4a1 1 0 0 0-1-1m-9.71 1.71a1 1 0 0 0 .33.21a.94.94 0 0 0 .76 0a1 1 0 0 0 .33-.21l4-4a1 1 0 0 0-1.42-1.42L13 12.59V3a1 1 0 0 0-2 0v9.59l-2.29-2.3a1 1 0 1 0-1.42 1.42Z"/></svg>`
  },
  {
    id: "kmind-icon://builtin/ui/keyboard",
    group: "ui",
    name: "keyboard",
    label: "Shortcuts",
    catalog: { "groupId": "ui", "groupLabel": "UI", "order": 300, "surfaces": ["external-link", "host-ui", "editor-ui"] },
    viewBox: "0 0 24 24",
    svg: `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="100%" height="100%" aria-hidden="true" focusable="false"><path fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M2 11c0-2.828 0-4.243.879-5.121C3.757 5 5.172 5 8 5h8c2.828 0 4.243 0 5.121.879C22 6.757 22 8.172 22 11v2c0 2.828 0 4.243-.879 5.121C20.243 19 18.828 19 16 19H8c-2.828 0-4.243 0-5.121-.879C2 17.243 2 15.828 2 13zm5 5h10M5 9h3m3 0h3m3 0h2M5 12h2m3 0h3m3 0h3"/></svg>`
  },
  {
    id: "kmind-icon://builtin/ui/link",
    group: "ui",
    name: "link",
    label: "Link",
    catalog: { "groupId": "ui", "groupLabel": "UI", "order": 300, "surfaces": ["external-link", "host-ui", "editor-ui"] },
    viewBox: "0 0 24 24",
    svg: `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="100%" height="100%" aria-hidden="true" focusable="false"><path fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M21 3h-6.75M21 3v6.75M21 3l-8.25 8.25M9.4 3c-2.24 0-3.36 0-4.216.436a4 4 0 0 0-1.748 1.748C3 6.04 3 7.16 3 9.4v5.2c0 2.24 0 3.36.436 4.216a4 4 0 0 0 1.748 1.748C6.04 21 7.16 21 9.4 21h5.2c2.24 0 3.36 0 4.216-.436a4 4 0 0 0 1.748-1.748C21 17.96 21 16.84 21 14.6v-1.1"/></svg>`
  },
  {
    id: "kmind-icon://builtin/ui/minimap",
    group: "ui",
    name: "minimap",
    label: "Minimap",
    catalog: { "groupId": "ui", "groupLabel": "UI", "order": 300, "surfaces": ["external-link", "host-ui", "editor-ui"] },
    viewBox: "0 0 24 24",
    svg: `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="100%" height="100%" aria-hidden="true" focusable="false"><path fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M3 8.593c0-1.527 0-2.29.393-2.735c.139-.159.308-.285.497-.372c1.416-.653 3.272 1.066 4.77 1.013q.297-.011.587-.082c2.184-.535 3.552-3.08 5.798-3.39c1.287-.18 2.7.598 3.904 1.014c.99.342 1.485.513 1.768.92S21 5.91 21 6.99v8.422c0 1.526 0 2.29-.393 2.735a1.5 1.5 0 0 1-.497.371c-1.416.653-3.272-1.065-4.77-1.012a3 3 0 0 0-.587.081c-2.184.535-3.552 3.08-5.798 3.391c-1.281.178-4.847-.75-5.672-1.935C3 18.636 3 18.096 3 17.014zm6-2.052v14.255m6-17.615v14.255"/></svg>`
  },
  {
    id: "kmind-icon://builtin/ui/new",
    group: "ui",
    name: "new",
    label: "New",
    catalog: { "groupId": "ui", "groupLabel": "UI", "order": 300, "surfaces": ["external-link", "host-ui", "editor-ui"] },
    viewBox: "0 0 24 24",
    svg: `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="100%" height="100%" aria-hidden="true" focusable="false"><path fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M3 9v10.4c0 .56 0 .84.109 1.054a1 1 0 0 0 .437.437C3.76 21 4.04 21 4.598 21H15m-1-8v-3m0 0V7m0 3h-3m3 0h3M7 13.8V6.2c0-1.12 0-1.68.218-2.108c.192-.377.497-.682.874-.874C8.52 3 9.08 3 10.2 3h7.6c1.12 0 1.68 0 2.108.218a2 2 0 0 1 .874.874C21 4.52 21 5.08 21 6.2v7.6c0 1.12 0 1.68-.218 2.108a2 2 0 0 1-.874.874c-.428.218-.986.218-2.104.218h-7.607c-1.118 0-1.678 0-2.105-.218a2 2 0 0 1-.874-.874C7 15.48 7 14.92 7 13.8"/></svg>`
  },
  {
    id: "kmind-icon://builtin/ui/notes",
    group: "ui",
    name: "notes",
    label: "Notes",
    catalog: { "groupId": "ui", "groupLabel": "UI", "order": 300, "surfaces": ["external-link", "host-ui", "editor-ui"] },
    viewBox: "0 0 24 24",
    svg: `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="100%" height="100%" aria-hidden="true" focusable="false"><path fill="currentColor" d="M4 4a2 2 0 0 1 2-2h8a1 1 0 0 1 .707.293l5 5A1 1 0 0 1 20 8v12a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2zm13.586 4L14 4.414V8zM12 4H6v16h12V10h-5a1 1 0 0 1-1-1zm-4 9a1 1 0 0 1 1-1h6a1 1 0 1 1 0 2H9a1 1 0 0 1-1-1m0 4a1 1 0 0 1 1-1h6a1 1 0 1 1 0 2H9a1 1 0 0 1-1-1"/></svg>`
  },
  {
    id: "kmind-icon://builtin/ui/open",
    group: "ui",
    name: "open",
    label: "Open",
    catalog: { "groupId": "ui", "groupLabel": "UI", "order": 300, "surfaces": ["external-link", "host-ui", "editor-ui"] },
    viewBox: "0 0 24 24",
    svg: `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="100%" height="100%" aria-hidden="true" focusable="false"><g fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="1.75"><path d="M9 7.5H7.75A2.75 2.75 0 0 0 5 10.25v6A2.75 2.75 0 0 0 7.75 19h6A2.75 2.75 0 0 0 16.5 16.25V15" opacity="0.5" /><path d="M10 14 19 5" /><path d="M13.5 5H19v5.5" /></g></svg>`
  },
  {
    id: "kmind-icon://builtin/ui/open-bottom",
    group: "ui",
    name: "open-bottom",
    label: "Open Bottom",
    catalog: { "groupId": "ui", "groupLabel": "UI", "order": 300, "surfaces": ["external-link", "host-ui", "editor-ui"] },
    viewBox: "0 0 24 24",
    svg: `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="100%" height="100%" aria-hidden="true" focusable="false"><g fill="none" stroke="currentColor" stroke-width="1.5" transform="rotate(90 12 12)"><path d="M12 21h1c3.771 0 5.657 0 6.828-1.172S21 16.771 21 13v-2c0-3.771 0-5.657-1.172-6.828S16.771 3 13 3h-1" /><path d="M13 21H9c-2.828 0-4.243 0-5.121-.879C3 19.243 3 17.828 3 15V9c0-2.828 0-4.243.879-5.121C4.757 3 6.172 3 9 3h4" opacity="0.5" stroke-dasharray="2.5 3" stroke-linecap="round" /><path d="M12 22V2" stroke-linecap="round" /></g></svg>`
  },
  {
    id: "kmind-icon://builtin/ui/open-right",
    group: "ui",
    name: "open-right",
    label: "Open Right",
    catalog: { "groupId": "ui", "groupLabel": "UI", "order": 300, "surfaces": ["external-link", "host-ui", "editor-ui"] },
    viewBox: "0 0 24 24",
    svg: `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="100%" height="100%" aria-hidden="true" focusable="false"><g fill="none" stroke="currentColor" stroke-width="1.5"><path d="M12 21h1c3.771 0 5.657 0 6.828-1.172S21 16.771 21 13v-2c0-3.771 0-5.657-1.172-6.828S16.771 3 13 3h-1"/><path stroke-dasharray="2.5 3" stroke-linecap="round" d="M13 21H9c-2.828 0-4.243 0-5.121-.879C3 19.243 3 17.828 3 15V9c0-2.828 0-4.243.879-5.121C4.757 3 6.172 3 9 3h4" opacity="0.5"/><path stroke-linecap="round" d="M12 22V2"/></g></svg>`
  },
  {
    id: "kmind-icon://builtin/ui/pdf",
    group: "ui",
    name: "pdf",
    label: "PDF",
    catalog: { "groupId": "ui", "groupLabel": "UI", "order": 300, "surfaces": ["external-link", "host-ui", "editor-ui"] },
    viewBox: "0 0 16 16",
    svg: `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 16 16" width="100%" height="100%" aria-hidden="true" focusable="false"><path fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" d="M2.8 14.34c1.81-1.25 3.02-3.16 3.91-5.5.9-2.33 1.86-4.33 1.44-6.63-.06-.36-.57-.73-.83-.7-1.02.06-.95 1.21-.85 1.9.24 1.71 1.56 3.7 2.84 5.56 1.27 1.87 2.32 2.16 3.78 2.26.5.03 1.25-.14 1.37-.58.77-2.8-9.02-.54-12.28 2.08-.4.33-.86 1-.6 1.46.2.36.87.4 1.23.15Z"/></svg>`
  },
  {
    id: "kmind-icon://builtin/ui/preview",
    group: "ui",
    name: "preview",
    label: "Preview",
    catalog: { "groupId": "ui", "groupLabel": "UI", "order": 300, "surfaces": ["external-link", "host-ui", "editor-ui"] },
    viewBox: "0 0 24 24",
    svg: `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="100%" height="100%" aria-hidden="true" focusable="false"><g fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="1.75"><path d="M2.75 12s3.3-5.5 9.25-5.5 9.25 5.5 9.25 5.5-3.3 5.5-9.25 5.5S2.75 12 2.75 12Z" /><circle cx="12" cy="12" r="2.75" /></g></svg>`
  },
  {
    id: "kmind-icon://builtin/ui/project",
    group: "ui",
    name: "project",
    label: "Project",
    catalog: { "groupId": "ui", "groupLabel": "UI", "order": 300, "surfaces": ["external-link", "host-ui", "editor-ui"] },
    viewBox: "0 0 24 24",
    svg: `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="100%" height="100%" aria-hidden="true" focusable="false"><path fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="1" d="M12 18.5L9 17l-6 3V7l6-3l6 3l6-3v8M9 4v13m6-10v6.5m2.001 5.5a2 2 0 1 0 4 0a2 2 0 1 0-4 0m2-3.5V17m0 4v1.5m3.031-5.25l-1.299.75m-3.463 2l-1.3.75m0-3.5l1.3.75m3.463 2l1.3.75"/></svg>`
  },
  {
    id: "kmind-icon://builtin/ui/projects",
    group: "ui",
    name: "projects",
    label: "Projects",
    catalog: { "groupId": "ui", "groupLabel": "UI", "order": 300, "surfaces": ["external-link", "host-ui", "editor-ui"] },
    viewBox: "0 0 24 24",
    svg: `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="100%" height="100%" aria-hidden="true" focusable="false"><path fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M19 7h-7.34a2 2 0 0 1-1.322-.5l-2.272-2M19 7a2 2 0 0 1 2 2v9a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V6a2 2 0 0 1 2-2h1.745a2 2 0 0 1 1.322.5M19 7a2.5 2.5 0 0 0-2.5-2.5H8.066"/></svg>`
  },
  {
    id: "kmind-icon://builtin/ui/read-only",
    group: "ui",
    name: "read-only",
    label: "Read-only",
    catalog: { "groupId": "ui", "groupLabel": "UI", "order": 300, "surfaces": ["external-link", "host-ui", "editor-ui"] },
    viewBox: "0 0 24 24",
    svg: `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="100%" height="100%" aria-hidden="true" focusable="false"><path fill="currentColor" d="M16 8a3 3 0 0 1 3 3v8a3 3 0 0 1-3 3H7a3 3 0 0 1-3-3v-8a3 3 0 0 1 3-3V6.5C7 4 9 2 11.5 2S16 4 16 6.5zM7 9a2 2 0 0 0-2 2v8a2 2 0 0 0 2 2h9a2 2 0 0 0 2-2v-8a2 2 0 0 0-2-2zm8-1V6.5A3.5 3.5 0 0 0 11.5 3A3.5 3.5 0 0 0 8 6.5V8zm-3.5 6a1.5 1.5 0 0 0-1.5 1.5a1.5 1.5 0 0 0 1.5 1.5a1.5 1.5 0 0 0 1.5-1.5a1.5 1.5 0 0 0-1.5-1.5m0-1a2.5 2.5 0 0 1 2.5 2.5a2.5 2.5 0 0 1-2.5 2.5A2.5 2.5 0 0 1 9 15.5a2.5 2.5 0 0 1 2.5-2.5"/></svg>`
  },
  {
    id: "kmind-icon://builtin/ui/redo",
    group: "ui",
    name: "redo",
    label: "Redo",
    catalog: { "groupId": "ui", "groupLabel": "UI", "order": 300, "surfaces": ["external-link", "host-ui", "editor-ui"] },
    viewBox: "0 0 24 24",
    svg: `<svg viewBox="0 0 24 24" aria-hidden="true" focusable="false" width="100%" height="100%"><path d="M15 6l4 4-4 4" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/><path d="M19 10h-8a5 5 0 1 0 0 10h4" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>`
  },
  {
    id: "kmind-icon://builtin/ui/relation",
    group: "ui",
    name: "relation",
    label: "Relation",
    catalog: { "groupId": "ui", "groupLabel": "UI", "order": 300, "surfaces": ["external-link", "host-ui", "editor-ui"] },
    viewBox: "0 0 24 24",
    svg: `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="100%" height="100%" aria-hidden="true" focusable="false"><path fill="currentColor" d="M13 8v8a3 3 0 0 1-3 3H7.83a3.001 3.001 0 1 1 0-2H10a1 1 0 0 0 1-1V8a3 3 0 0 1 3-3h3V2l5 4l-5 4V7h-3a1 1 0 0 0-1 1M5 19a1 1 0 1 0 0-2a1 1 0 0 0 0 2"/></svg>`
  },
  {
    id: "kmind-icon://builtin/ui/search",
    group: "ui",
    name: "search",
    label: "Search",
    catalog: { "groupId": "ui", "groupLabel": "UI", "order": 300, "surfaces": ["external-link", "host-ui", "editor-ui"] },
    viewBox: "0 0 24 24",
    svg: `<svg viewBox="0 0 24 24" aria-hidden="true" focusable="false" width="100%" height="100%"><circle cx="11" cy="11" r="7" fill="none" stroke="currentColor" stroke-width="2"/><path d="M16.5 16.5L20 20" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"/></svg>`
  },
  {
    id: "kmind-icon://builtin/ui/style",
    group: "ui",
    name: "style",
    label: "Style",
    catalog: { "groupId": "ui", "groupLabel": "UI", "order": 300, "surfaces": ["external-link", "host-ui", "editor-ui"] },
    viewBox: "0 0 24 24",
    svg: `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="100%" height="100%" aria-hidden="true" focusable="false"><path fill="currentColor" d="M20.063 8.445a3.22 3.22 0 0 1-.002 4.551l-7.123 7.112a2.25 2.25 0 0 1-.943.562l-4.293 1.29a1 1 0 0 1-1.24-1.264l1.362-4.228c.11-.34.3-.65.552-.903l7.133-7.121a3.22 3.22 0 0 1 4.554.002m-3.494 1.06l-7.133 7.12a.75.75 0 0 0-.184.301l-1.07 3.323l3.382-1.015a.75.75 0 0 0 .314-.188L19 11.936a1.718 1.718 0 1 0-2.431-2.432M8.15 2.37l.05.105l3.253 8.249l-1.157 1.155L9.556 10H5.443l-.995 2.52a.75.75 0 0 1-.876.454l-.098-.031a.75.75 0 0 1-.452-.876l.03-.098l3.754-9.495a.75.75 0 0 1 1.345-.104m-.648 2.422L6.036 8.5h2.928z"/></svg>`
  },
  {
    id: "kmind-icon://builtin/ui/submap",
    group: "ui",
    name: "submap",
    label: "SubMap",
    catalog: { "groupId": "ui", "groupLabel": "UI", "order": 300, "surfaces": ["external-link", "host-ui", "editor-ui"] },
    viewBox: "0 0 24 24",
    svg: `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="100%" height="100%" aria-hidden="true" focusable="false"><path fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="1.2" d="m11 19l-1.106-.552a2 2 0 0 0-1.788 0l-3.659 1.83A1 1 0 0 1 3 19.381V6.618a1 1 0 0 1 .553-.894l4.553-2.277a2 2 0 0 1 1.788 0l4.212 2.106a2 2 0 0 0 1.788 0l3.659-1.83A1 1 0 0 1 21 4.619V12m-6-6.236V12m3 3v6m3-3h-6M9 3.236v15"/></svg>`
  },
  {
    id: "kmind-icon://builtin/ui/summary",
    group: "ui",
    name: "summary",
    label: "Summary",
    catalog: { "groupId": "ui", "groupLabel": "UI", "order": 300, "surfaces": ["external-link", "host-ui", "editor-ui"] },
    viewBox: "0 0 24 24",
    svg: `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="100%" height="100%" aria-hidden="true" focusable="false"><path fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="1.2" d="M9 20.25a3 3 0 0 1-3-3v0v-1.343a4 4 0 0 0-1.172-2.829L3.75 12l1.078-1.078A4 4 0 0 0 6 8.093V6.75v0a3 3 0 0 1 3-3v0m6 16.5a3 3 0 0 0 3-3v0v-1.343a4 4 0 0 1 1.172-2.829L20.25 12l-1.078-1.078A4 4 0 0 1 18 8.093V6.75v0a3 3 0 0 0-3-3v0"/></svg>`
  },
  {
    id: "kmind-icon://builtin/ui/switch-card",
    group: "ui",
    name: "switch-card",
    label: "Switch To Card",
    catalog: { "groupId": "ui", "groupLabel": "UI", "order": 300, "surfaces": ["external-link", "host-ui", "editor-ui"] },
    viewBox: "0 0 24 24",
    svg: `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="100%" height="100%" aria-hidden="true" focusable="false"><g fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="1.75"><rect x="4.5" y="5.5" width="15" height="13" rx="2.5" /><path d="M4.5 9.5h15" /><path d="M8 13.25h8" opacity="0.7" /><path d="M8 16h4.5" opacity="0.7" /></g></svg>`
  },
  {
    id: "kmind-icon://builtin/ui/switch-live",
    group: "ui",
    name: "switch-live",
    label: "Switch To Live",
    catalog: { "groupId": "ui", "groupLabel": "UI", "order": 300, "surfaces": ["external-link", "host-ui", "editor-ui"] },
    viewBox: "0 0 24 24",
    svg: `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="100%" height="100%" aria-hidden="true" focusable="false"><g fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="1.75"><path d="M8 4H4v4M16 4h4v4M4 16v4h4M20 16v4h-4" /><circle cx="12" cy="12" r="2.25" /></g></svg>`
  },
  {
    id: "kmind-icon://builtin/ui/tags",
    group: "ui",
    name: "tags",
    label: "Tags",
    catalog: { "groupId": "ui", "groupLabel": "UI", "order": 300, "surfaces": ["external-link", "host-ui", "editor-ui"] },
    viewBox: "0 0 24 24",
    svg: `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="100%" height="100%" aria-hidden="true" focusable="false"><path fill="currentColor" fill-rule="evenodd" d="M3.207 14.207a1 1 0 0 1 0-1.414l9.5-9.5A1 1 0 0 1 13.414 3H20a1 1 0 0 1 1 1v6.586a1 1 0 0 1-.293.707l-9.5 9.5a1 1 0 0 1-1.414 0zM19.8 10.503V4.2h-6.303l-9.3 9.3l6.303 6.303zM16 9.5a1.5 1.5 0 1 1 0-3a1.5 1.5 0 0 1 0 3"/></svg>`
  },
  {
    id: "kmind-icon://builtin/ui/theme",
    group: "ui",
    name: "theme",
    label: "Theme",
    catalog: { "groupId": "ui", "groupLabel": "UI", "order": 300, "surfaces": ["external-link", "host-ui", "editor-ui"] },
    viewBox: "0 0 24 24",
    svg: `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="100%" height="100%" aria-hidden="true" focusable="false"><path fill="currentColor" d="M11 13.5v8H3v-8zm-2 2H5v4h4zM12 2l5.5 9h-11zm0 3.86L10.08 9h3.84zM17.5 13c2.5 0 4.5 2 4.5 4.5S20 22 17.5 22S13 20 13 17.5s2-4.5 4.5-4.5m0 2a2.5 2.5 0 0 0-2.5 2.5a2.5 2.5 0 0 0 2.5 2.5a2.5 2.5 0 0 0 2.5-2.5a2.5 2.5 0 0 0-2.5-2.5"/></svg>`
  },
  {
    id: "kmind-icon://builtin/ui/unbind",
    group: "ui",
    name: "unbind",
    label: "Unbind",
    catalog: { "groupId": "ui", "groupLabel": "UI", "order": 300, "surfaces": ["external-link", "host-ui", "editor-ui"] },
    viewBox: "0 0 24 24",
    svg: `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="100%" height="100%" aria-hidden="true" focusable="false"><path fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 20v-2m2-2h2M7.05 11.293l-1.414 1.414a4 4 0 0 0 5.657 5.657l1.415-1.414M6 8H4m4-4v2m3.293 1.05l1.414-1.414a4 4 0 1 1 5.656 5.657l-1.414 1.414" /></svg>`
  },
  {
    id: "kmind-icon://builtin/ui/undo",
    group: "ui",
    name: "undo",
    label: "Undo",
    catalog: { "groupId": "ui", "groupLabel": "UI", "order": 300, "surfaces": ["external-link", "host-ui", "editor-ui"] },
    viewBox: "0 0 24 24",
    svg: `<svg viewBox="0 0 24 24" aria-hidden="true" focusable="false" width="100%" height="100%"><path d="M9 14L5 10l4-4" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/><path d="M5 10h8a5 5 0 1 1 0 10H9" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>`
  },
  {
    id: "kmind-icon://builtin/ui/zen",
    group: "ui",
    name: "zen",
    label: "Zen",
    catalog: { "groupId": "ui", "groupLabel": "UI", "order": 300, "surfaces": ["external-link", "host-ui", "editor-ui"] },
    viewBox: "0 0 24 24",
    svg: `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="100%" height="100%" aria-hidden="true" focusable="false"><path fill="currentColor" d="M12 13.5q.214 0 .357-.144T12.5 13V8q0-.213-.144-.356t-.357-.144t-.356.144T11.5 8v5q0 .213.144.356t.357.144m3-1.5q.213 0 .356-.144t.143-.356V9q0-.213-.144-.356t-.357-.144t-.356.144T14.5 9v2.5q0 .213.144.356t.357.144m-6-.5q.213 0 .356-.144T9.5 11V9q0-.213-.144-.356T8.999 8.5t-.356.144T8.5 9v2q0 .213.144.356t.357.144M7 17.238q-1.425-1.3-2.212-2.922T4 10.986q0-3.327 2.333-5.657T12 3q2.702 0 4.884 1.645t2.83 4.25l1.036 4.103q.1.38-.142.692q-.242.31-.646.31H18v3.385q0 .666-.475 1.14t-1.14.475H14v1.5q0 .213-.144.356t-.357.144t-.356-.144T13 20.5v-1.683q0-.357.232-.587t.576-.23h2.577q.269 0 .442-.173t.173-.442v-3.577q0-.344.232-.576t.576-.232H19.7l-.95-3.875q-.575-2.294-2.47-3.71Q14.388 4 12 4Q9.1 4 7.05 6.03Q5 8.062 5 10.97q0 1.494.613 2.84q.612 1.346 1.737 2.392L8 16.8v3.7q0 .213-.144.356T7.499 21t-.356-.144T7 20.5zm5.35-4.738"/></svg>`
  },
  {
    id: "kmind-icon://builtin/ui/zoom-in",
    group: "ui",
    name: "zoom-in",
    label: "Zoom In",
    catalog: { "groupId": "ui", "groupLabel": "UI", "order": 300, "surfaces": ["external-link", "host-ui", "editor-ui"] },
    viewBox: "0 0 24 24",
    svg: `<svg viewBox="0 0 24 24" aria-hidden="true" focusable="false" width="100%" height="100%"><circle cx="11" cy="11" r="7" fill="none" stroke="currentColor" stroke-width="2"/><path d="M16.5 16.5L20 20" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"/><path d="M11 8v6M8 11h6" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"/></svg>`
  },
  {
    id: "kmind-icon://builtin/ui/zoom-out",
    group: "ui",
    name: "zoom-out",
    label: "Zoom Out",
    catalog: { "groupId": "ui", "groupLabel": "UI", "order": 300, "surfaces": ["external-link", "host-ui", "editor-ui"] },
    viewBox: "0 0 24 24",
    svg: `<svg viewBox="0 0 24 24" aria-hidden="true" focusable="false" width="100%" height="100%"><circle cx="11" cy="11" r="7" fill="none" stroke="currentColor" stroke-width="2"/><path d="M16.5 16.5L20 20" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"/><path d="M8 11h6" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"/></svg>`
  }
];

// ../icons/src/index.ts
var ICON_BY_ID = /* @__PURE__ */ new Map();
for (const icon of BUILTIN_ICONS) {
  ICON_BY_ID.set(icon.id, icon);
  for (const alias of icon.aliases ?? []) {
    ICON_BY_ID.set(alias, icon);
  }
}

// ../app/src/utils/node-links.ts
init_src();

// ../app/src/features/node-clipboard-feature.ts
init_src();

// ../app/src/services/document-markdown.ts
function buildMarkdownSubtree(doc, rootId) {
  const lines = [];
  const walk = (nodeId, depth) => {
    const node = doc.nodes[nodeId];
    if (!node) return;
    const indent = "  ".repeat(Math.max(0, depth));
    const text = String(node.text ?? "").trim();
    lines.push(`${indent}- ${text.length > 0 ? text : "#"}`);
    for (const childId of node.children) {
      if (!doc.nodes[childId]) continue;
      walk(childId, depth + 1);
    }
  };
  walk(rootId, 0);
  return lines.join("\n").trim() + "\n";
}
function buildMindMapDocumentMarkdown(doc, rootIds) {
  const ids = Array.isArray(rootIds) && rootIds.length > 0 ? rootIds : doc.roots;
  return ids.map((rootId) => buildMarkdownSubtree(doc, rootId)).join("\n").trim() + "\n";
}

// ../app/src/features/node-width-feature.ts
init_src();

// ../app/src/features/theme-feature.ts
init_src();

// ../app/src/themes/resolve-apply-target.ts
init_src();

// ../app/src/themes/theme-package-v1.ts
init_src();
var KMIND_THEME_PACKAGE_MAX_BYTES = 512 * 1024;

// ../app/src/features/layout-feature.ts
init_src();

// ../app/src/features/context-menu-feature.ts
init_src();

// ../app/src/services/import-legacy-kmind.ts
init_src();

// ../app/src/services/import-builders.ts
init_src();
function buildThemeTemplate(args) {
  const theme = args.templateDoc.theme;
  if (!theme || theme.schemaVersion !== 1) return null;
  const next = {
    schemaVersion: 1,
    defaultTheme: theme.defaultTheme,
    appearance: theme.appearance,
    rainbow: theme.rainbow ? { enabled: theme.rainbow.enabled, paletteOverride: theme.rainbow.paletteOverride } : void 0
  };
  const oldRootId = args.templateDoc.roots[0];
  if (oldRootId && args.newRootIds.length > 0) {
    const edgeRoute = theme.rootEdgeRoutes?.[oldRootId];
    if (edgeRoute) {
      next.rootEdgeRoutes = Object.fromEntries(args.newRootIds.map((rootId) => [rootId, edgeRoute]));
    }
    const rainbowEnabled = theme.rootRainbowEdges?.[oldRootId];
    if (typeof rainbowEnabled === "boolean") {
      next.rootRainbowEdges = Object.fromEntries(args.newRootIds.map((rootId) => [rootId, rainbowEnabled]));
    }
  }
  return next;
}
function applyTemplateDocToImportedDocument(args) {
  let doc = args.doc;
  const templateDoc = args.templateDoc;
  const rootIds = doc.roots.filter((rootId) => Boolean(doc.nodes[rootId]));
  if (templateDoc) {
    const settings = getProjectSettingsV1(templateDoc);
    if (settings) {
      doc = upsertProjectSettingsV1(doc, settings);
      doc = applyProjectDefaultRootLayoutV1({ doc, defaultRootLayout: settings.defaultRootLayout }).doc;
    }
    const theme = buildThemeTemplate({ templateDoc, newRootIds: rootIds });
    if (theme) doc = { ...doc, theme };
  }
  return ensureProjectManifestV1(doc).doc;
}
function createDocumentFromSubtree(args) {
  const idGenerator = new DefaultIdGenerator();
  const baseDoc = createDocument(idGenerator, { rootText: args.rootText || "Root" });
  const core = new MindMapCore({ idGenerator, initialDocument: baseDoc });
  const rootId = core.getState().document.roots[0];
  if (rootId && args.subtree.roots.length > 0) {
    core.dispatch({
      type: "insert_subtree",
      payload: {
        parentId: rootId,
        subtree: {
          roots: args.subtree.roots,
          nodes: args.subtree.nodes,
          assets: args.subtree.assets ?? {}
        }
      }
    });
  }
  const doc = core.toJSON();
  return applyTemplateDocToImportedDocument({ doc, templateDoc: args.templateDoc });
}

// ../app/src/services/import-xmind.ts
init_src();

// ../app/src/services/kmindz-project-v3-interop.ts
function buildDocumentZipV1BytesFromKmindzProjectV3(args) {
  const payload = args.payload;
  const docsZipB64 = payload.docsZipB64;
  if (!docsZipB64) {
    throw new Error("Invalid kmindz v3 payload: missing docs pack (metadata#kmindz-docs).");
  }
  const docsZipBytes = decodeBase64(docsZipB64);
  const docsZipMap = readZipStore(docsZipBytes);
  const docsManifestBytes = docsZipMap.get("manifest.json");
  if (!docsManifestBytes) throw new Error("Invalid kmindz docs pack: missing manifest.json.");
  const docsManifestParsed = JSON.parse(decodeUtf8(docsManifestBytes));
  if (docsManifestParsed.schemaVersion !== 1) {
    throw new Error(`Unsupported kmindz docs pack schema: ${String(docsManifestParsed.schemaVersion ?? "")}`);
  }
  const sourceRootDocId = typeof docsManifestParsed.rootDocId === "string" ? docsManifestParsed.rootDocId.trim() : "";
  if (!sourceRootDocId) throw new Error("Invalid kmindz docs pack: missing rootDocId.");
  const docsEntries = Array.isArray(docsManifestParsed.documents) ? docsManifestParsed.documents : [];
  const documents = [];
  for (const entry of docsEntries) {
    if (!entry || typeof entry !== "object") continue;
    const id = String(entry.id ?? "").trim();
    const title = String(entry.title ?? "").trim() || "Untitled";
    const path6 = String(entry.path ?? "").trim();
    if (!id || !path6) continue;
    const bytes = docsZipMap.get(path6);
    if (!bytes) throw new Error(`Invalid kmindz docs pack: missing doc file: ${path6}`);
    documents.push({ id, title, path: path6, bytes });
  }
  if (!documents.some((doc) => doc.id === sourceRootDocId)) {
    throw new Error(`Invalid kmindz docs pack: missing root doc: ${sourceRootDocId}`);
  }
  const assets = [];
  if (payload.assetsZipB64) {
    const assetsZipBytes = decodeBase64(payload.assetsZipB64);
    const assetsZipMap = readZipStore(assetsZipBytes);
    const indexBytes = assetsZipMap.get("index.json");
    if (indexBytes) {
      const indexParsed = JSON.parse(decodeUtf8(indexBytes));
      if (indexParsed.schemaVersion === 1 && indexParsed.assets && typeof indexParsed.assets === "object") {
        for (const [assetId, entry] of Object.entries(indexParsed.assets)) {
          if (!entry) continue;
          const mimeType = String(entry.mimeType ?? "").trim();
          const path6 = String(entry.path ?? "").trim();
          const size = Number(entry.size ?? 0);
          if (!mimeType || !path6) continue;
          if (!Number.isFinite(size) || size < 0) continue;
          const bytes = assetsZipMap.get(path6);
          if (!bytes) continue;
          const contentHash = String(entry.contentHash ?? "").trim();
          const ext = String(entry.ext ?? "").trim();
          assets.push({ id: assetId, path: path6, mimeType, size, bytes, ...contentHash ? { contentHash } : {}, ...ext ? { ext } : {} });
        }
      }
    }
  }
  const collabBytes = (() => {
    const b64 = String(payload.collabUpdateB64 ?? "").trim();
    if (!b64) return null;
    try {
      return decodeBase64(b64);
    } catch {
      return null;
    }
  })();
  const collabPath = "collab/yjs.update";
  const resolveRootTitle = () => {
    const fromHeader = payload.header.documentsMeta?.[sourceRootDocId]?.title;
    if (typeof fromHeader === "string" && fromHeader.trim()) return fromHeader.trim();
    const fromManifest = documents.find((doc) => doc.id === sourceRootDocId)?.title ?? "";
    return fromManifest.trim() || "KMind";
  };
  const manifest = {
    schemaVersion: 1,
    createdAt: Date.now(),
    app: { name: "kmind-zen", version: null },
    rootDocId: sourceRootDocId,
    documents: documents.map((doc) => ({ id: doc.id, title: doc.title, path: doc.path })),
    assets: assets.map((asset) => ({ id: asset.id, path: asset.path, mimeType: asset.mimeType, size: asset.size, ...asset.contentHash ? { contentHash: asset.contentHash } : {}, ...asset.ext ? { ext: asset.ext } : {} })),
    ...collabBytes ? { collab: { kind: "yjs", schemaVersion: 1, path: collabPath, size: collabBytes.byteLength } } : {},
    document: {
      id: sourceRootDocId,
      title: resolveRootTitle()
    }
  };
  const uniqueFileBytesByPath = /* @__PURE__ */ new Map();
  const addFile = (path6, bytes) => {
    if (!path6) return;
    if (uniqueFileBytesByPath.has(path6)) return;
    uniqueFileBytesByPath.set(path6, bytes);
  };
  for (const doc of documents) addFile(doc.path, doc.bytes);
  for (const asset of assets) addFile(asset.path, asset.bytes);
  if (collabBytes) addFile(collabPath, collabBytes);
  const files = [
    { path: "manifest.json", bytes: encodeUtf8(JSON.stringify(manifest, null, 2)) },
    ...Array.from(uniqueFileBytesByPath.entries()).sort((a, b) => a[0].localeCompare(b[0])).map(([path6, bytes]) => ({ path: path6, bytes }))
  ];
  return createZipStore(files);
}

// ../app/src/index.ts
init_src();
init_src();
init_src();

// ../app/src/themes/theme-designer-draft.ts
init_src();

// ../app/src/themes/theme-designer-descriptors.ts
var WEBAPP_OPEN_EDGE_ROUTE_TYPES = [
  "cubic",
  "quadratic",
  "center-quadratic",
  "center-quadratic-tapered",
  "edge-lead-quadratic",
  "edge-lead-quadratic-tapered",
  "straight",
  "orthogonal",
  "orthogonal-rounded",
  "tapered"
];
var THEME_DESIGNER_EDGE_ROUTE_LABELS = {
  cubic: "Cubic",
  quadratic: "Quadratic",
  "center-quadratic": "Center Quadratic",
  "center-quadratic-tapered": "Center Tapered",
  "edge-lead-quadratic": "Lead Quadratic",
  "edge-lead-quadratic-tapered": "Lead Tapered",
  straight: "Straight",
  orthogonal: "Orthogonal",
  "orthogonal-rounded": "Rounded Orthogonal",
  tapered: "Tapered"
};
var THEME_DESIGNER_EDGE_ROUTES = WEBAPP_OPEN_EDGE_ROUTE_TYPES.map((value) => ({
  value,
  label: THEME_DESIGNER_EDGE_ROUTE_LABELS[value]
}));

// ../app/src/services/markdown-headings.ts
function trimBlankLines(text) {
  const lines = String(text ?? "").split(/\r?\n/);
  let start = 0;
  while (start < lines.length && lines[start]?.trim().length === 0) start += 1;
  let end = lines.length - 1;
  while (end >= start && lines[end]?.trim().length === 0) end -= 1;
  return lines.slice(start, end + 1).join("\n");
}
function buildNotesContent(body, args) {
  const trimmed = trimBlankLines(body);
  if (trimmed.length === 0) return null;
  const notes = {
    id: args.id,
    type: "notes",
    region: "right",
    order: 0,
    text: trimmed
  };
  return { schemaVersion: 1, kind: "blocks", blocks: [notes] };
}
function buildSubtreeFromMarkdownHeadings(markdown) {
  const lines = String(markdown ?? "").split(/\r?\n/);
  const sections = [];
  for (const rawLine of lines) {
    const line = String(rawLine ?? "");
    const match = /^(#{1,6})\s+(.*)$/.exec(line);
    if (!match) {
      const last = sections[sections.length - 1];
      if (last) last.bodyLines.push(line);
      continue;
    }
    const level = match[1]?.length ?? 0;
    const title = String(match[2] ?? "").trim();
    sections.push({ level, title, bodyLines: [] });
  }
  if (sections.length === 0) return null;
  const nodes = {};
  const roots = [];
  const stack = [];
  for (let i = 0; i < sections.length; i += 1) {
    const section = sections[i];
    const id = `md_${i + 1}`;
    const content = buildNotesContent(section.bodyLines.join("\n"), { id: `notes_${i + 1}` });
    const targetStackLength = Math.max(0, section.level - 1);
    stack.splice(targetStackLength);
    const parentId = stack[targetStackLength - 1] ?? null;
    nodes[id] = {
      id,
      children: [],
      text: section.title,
      content: content ?? void 0,
      parentId: parentId ?? void 0
    };
    if (parentId) {
      const parent = nodes[parentId];
      if (parent) parent.children.push(id);
    } else {
      roots.push(id);
    }
    stack[targetStackLength] = id;
  }
  return { roots, nodes };
}

// ../app/src/services/import-markdown-headings.ts
function normalizeRootText(value, fallback) {
  const trimmed = typeof value === "string" ? value.trim() : "";
  return trimmed.length > 0 ? trimmed : fallback;
}
function createDocumentFromMarkdownHeadings(args) {
  const subtree = buildSubtreeFromMarkdownHeadings(args.markdown);
  if (!subtree) return { ok: false, error: "No markdown headings found." };
  const fallback = normalizeRootText(args.fallbackRootText, "Imported Markdown");
  const singleRootId = subtree.roots.length === 1 ? subtree.roots[0] : null;
  const singleRootNode = singleRootId ? subtree.nodes[singleRootId] ?? null : null;
  const rootText = singleRootNode ? normalizeRootText(singleRootNode.text, fallback) : fallback;
  const roots = (() => {
    if (!singleRootNode) return subtree.roots;
    return Array.isArray(singleRootNode.children) ? singleRootNode.children : [];
  })();
  const nodes = (() => {
    if (!singleRootId) return subtree.nodes;
    const next = { ...subtree.nodes };
    delete next[singleRootId];
    return next;
  })();
  let doc = createDocumentFromSubtree({
    rootText,
    subtree: { roots, nodes, assets: {} },
    templateDoc: args.templateDoc
  });
  const rootId = doc.roots[0];
  if (singleRootNode?.content && rootId) {
    const root = doc.nodes[rootId];
    if (root) {
      doc = {
        ...doc,
        nodes: {
          ...doc.nodes,
          [rootId]: {
            ...root,
            content: singleRootNode.content
          }
        }
      };
    }
  }
  return { ok: true, doc, rootText };
}

// ../app/src/services/outline-projection-v1.ts
init_src();

// ../app/src/services/node-ref-resolver.ts
init_src();

// ../app/src/utils/submap-graph.ts
function collectOutgoingSubmapEdges(doc) {
  const edges = [];
  for (const node of Object.values(doc.nodes)) {
    const subMapId = typeof node.subMapId === "string" ? node.subMapId.trim() : "";
    if (!subMapId) continue;
    edges.push({ nodeId: node.id, docId: subMapId });
  }
  return edges;
}
async function collectReachableDocIds(args) {
  const visited = args.visited ?? /* @__PURE__ */ new Set();
  const queue = [args.rootDocId];
  const result2 = [];
  const includeRoot = args.includeRoot !== false;
  while (queue.length > 0) {
    const docId = queue.shift();
    if (!docId) break;
    if (visited.has(docId)) continue;
    visited.add(docId);
    const record = await args.documents.get(docId);
    if (!record) continue;
    if (includeRoot || docId !== args.rootDocId) {
      result2.push(record.id);
    }
    for (const edge of collectOutgoingSubmapEdges(record.doc)) {
      if (visited.has(edge.docId)) continue;
      queue.push(edge.docId);
    }
  }
  return result2;
}
async function collectProjectMapSummaries(args) {
  const rootId = String(args.rootDocId ?? "").trim();
  if (!rootId) return [];
  const rootRecord = await args.documents.get(rootId);
  if (!rootRecord) return [];
  const includeRoot = args.includeRoot !== false;
  const manifestSubmaps = getProjectManifestV1(rootRecord.doc)?.submaps ?? [];
  const visited = /* @__PURE__ */ new Set();
  const reachable = await collectReachableDocIds({ rootDocId: rootId, documents: args.documents, includeRoot: false, visited });
  const reachableFromDetachedRoots = [];
  for (const detachedRootId of manifestSubmaps) {
    const out = await collectReachableDocIds({ rootDocId: detachedRootId, documents: args.documents, includeRoot: false, visited });
    reachableFromDetachedRoots.push(...out);
  }
  const seen = /* @__PURE__ */ new Set();
  const ordered = [];
  const pushUnique = (id) => {
    const trimmed = String(id ?? "").trim();
    if (!trimmed) return;
    if (trimmed === rootId) return;
    if (seen.has(trimmed)) return;
    seen.add(trimmed);
    ordered.push(trimmed);
  };
  for (const id of manifestSubmaps) pushUnique(id);
  for (const docId of reachable) pushUnique(docId);
  for (const docId of reachableFromDetachedRoots) pushUnique(docId);
  const result2 = [];
  if (includeRoot) result2.push({ docId: rootRecord.id, title: rootRecord.title });
  for (const docId of ordered) {
    const record = await args.documents.get(docId);
    if (!record) continue;
    result2.push({ docId: record.id, title: record.title });
  }
  return result2;
}

// ../app/src/services/project-search-v1.ts
function normalizeQueryText(value) {
  return typeof value === "string" ? value : "";
}
function normalizeFields(fields) {
  const raw = fields ?? {};
  return {
    nodes: raw.nodes !== false,
    notes: raw.notes !== false,
    comments: raw.comments !== false
  };
}
function normalizeProjectSearchQuery(raw) {
  const query = raw ?? {};
  const options = query.options ?? {};
  const modeRaw = typeof options.mode === "string" ? options.mode : "plain";
  const mode = modeRaw === "regex" || modeRaw === "fuzzy" ? modeRaw : "plain";
  return {
    text: normalizeQueryText(query.text),
    options: {
      mode,
      fields: normalizeFields(options.fields),
      caseSensitive: Boolean(options.caseSensitive),
      wholeWord: Boolean(options.wholeWord)
    }
  };
}
function isAsciiWordChar(ch) {
  return /[A-Za-z0-9_]/.test(ch);
}
function isWholeWordMatch(text, start, end) {
  const before = start > 0 ? text[start - 1] : "";
  const after = end < text.length ? text[end] : "";
  const beforeWord = before ? isAsciiWordChar(before) : false;
  const afterWord = after ? isAsciiWordChar(after) : false;
  return !beforeWord && !afterWord;
}
function createPlainMatcher(args) {
  const queryText = args.caseSensitive ? args.query : args.query.toLowerCase();
  return {
    mode: "plain",
    queryText: args.query,
    matchAll: (text) => {
      const haystack = args.caseSensitive ? text : text.toLowerCase();
      const ranges = [];
      if (!queryText) return ranges;
      let index = 0;
      while (true) {
        const next = haystack.indexOf(queryText, index);
        if (next < 0) break;
        const end = next + queryText.length;
        if (!args.wholeWord || isWholeWordMatch(haystack, next, end)) {
          ranges.push({ start: next, end });
        }
        index = Math.max(end, next + 1);
        if (ranges.length >= 5e3) break;
      }
      return ranges;
    }
  };
}
function createRegexMatcher(args) {
  const trimmed = args.pattern.trim();
  if (!trimmed) return { matcher: createPlainMatcher({ query: "", caseSensitive: true, wholeWord: false }) };
  const flags = args.caseSensitive ? "g" : "gi";
  const source = args.wholeWord ? `\\b(?:${trimmed})\\b` : trimmed;
  let regex;
  try {
    regex = new RegExp(source, flags);
  } catch (error) {
    const message = error instanceof Error ? error.message : String(error);
    return { error: message || "Invalid regex" };
  }
  return {
    matcher: {
      mode: "regex",
      queryText: trimmed,
      matchAll: (text) => {
        const ranges = [];
        regex.lastIndex = 0;
        let safety = 0;
        while (true) {
          const match = regex.exec(text);
          if (!match) break;
          const start = match.index;
          const raw = match[0] ?? "";
          const end = start + raw.length;
          if (end > start) {
            ranges.push({ start, end });
          }
          if (raw.length === 0) {
            regex.lastIndex += 1;
          }
          safety += 1;
          if (safety > 1e4) break;
          if (ranges.length >= 5e3) break;
        }
        return ranges;
      }
    }
  };
}
function createFuzzyMatcher(args) {
  const queryText = args.caseSensitive ? args.query : args.query.toLowerCase();
  return {
    mode: "fuzzy",
    queryText: args.query,
    matchAll: (text) => {
      if (!queryText) return [];
      const haystack = args.caseSensitive ? text : text.toLowerCase();
      const ranges = [];
      let ti = 0;
      for (let qi = 0; qi < queryText.length; qi += 1) {
        const qch = queryText[qi];
        const found = haystack.indexOf(qch, ti);
        if (found < 0) return [];
        ranges.push({ start: found, end: found + 1 });
        ti = found + 1;
        if (ranges.length >= 2e3) break;
      }
      return ranges;
    }
  };
}
function createMatcher(query) {
  const text = query.text.trim();
  const caseSensitive = Boolean(query.options.caseSensitive);
  const wholeWord = Boolean(query.options.wholeWord);
  if (query.options.mode === "regex") {
    const resolved = createRegexMatcher({ pattern: text, caseSensitive, wholeWord });
    if ("error" in resolved) {
      return { matcher: createPlainMatcher({ query: "", caseSensitive: true, wholeWord: false }), error: resolved.error };
    }
    return { matcher: resolved.matcher, error: null };
  }
  if (query.options.mode === "fuzzy") {
    return { matcher: createFuzzyMatcher({ query: text, caseSensitive }), error: null };
  }
  return { matcher: createPlainMatcher({ query: text, caseSensitive, wholeWord }), error: null };
}
function buildSnippet(text, ranges) {
  const first = ranges[0];
  if (!first) return { text: "", ranges: [] };
  const maxLen = 140;
  const padding = 48;
  const start = Math.max(0, first.start - padding);
  const end = Math.min(text.length, first.end + padding);
  let snippetStart = start;
  let snippetEnd = end;
  if (snippetEnd - snippetStart > maxLen) {
    const idealStart = Math.max(0, first.start - Math.floor(maxLen / 2));
    snippetStart = idealStart;
    snippetEnd = Math.min(text.length, snippetStart + maxLen);
  }
  const snippetText = text.slice(snippetStart, snippetEnd);
  const snippetRanges = ranges.filter((r) => r.end > snippetStart && r.start < snippetEnd).slice(0, 64).map((r) => ({
    start: Math.max(0, r.start - snippetStart),
    end: Math.min(snippetText.length, r.end - snippetStart)
  })).filter((r) => r.end > r.start);
  return { text: snippetText, ranges: snippetRanges };
}
function extractPlainTextFromProseMirrorDoc(doc) {
  if (!doc || typeof doc !== "object" || Array.isArray(doc)) return "";
  const out = [];
  const walk = (node) => {
    if (!node || typeof node !== "object" || Array.isArray(node)) return;
    if (node.type === "text") {
      if (typeof node.text === "string") out.push(node.text);
      return;
    }
    if (node.type === "hardBreak") {
      out.push("\n");
      return;
    }
    const children = Array.isArray(node.content) ? node.content : [];
    for (const child of children) walk(child);
    if (node.type === "paragraph" || node.type === "heading" || node.type === "codeBlock" || node.type === "blockquote") {
      out.push("\n");
    }
  };
  walk(doc);
  return out.join("").replace(/\n{3,}/g, "\n\n").trimEnd();
}
function resolveNodeBodyText(node) {
  const content = node.content;
  if (content?.schemaVersion !== 1) return node.text;
  if (content.kind === "plain-text") return content.text ?? "";
  if (content.kind === "richtext") {
    return extractPlainTextFromProseMirrorDoc(content.doc) || node.text;
  }
  if (content.kind === "blocks") {
    const richtext = content.blocks.find((block) => block.type === "richtext");
    if (richtext && richtext.engine === "prosemirror") return extractPlainTextFromProseMirrorDoc(richtext.doc) || node.text;
    return node.text;
  }
  return node.text;
}
function resolveNotesText(node) {
  const content = node.content;
  if (content?.schemaVersion !== 1 || content.kind !== "blocks") return null;
  const notes = content.blocks.find((block) => block.type === "notes");
  if (!notes) return null;
  const candidate = notes;
  if (typeof candidate.text === "string") return candidate.text;
  if (candidate.engine === "prosemirror" && candidate.doc && typeof candidate.doc === "object" && !Array.isArray(candidate.doc)) {
    return extractPlainTextFromProseMirrorDoc(candidate.doc);
  }
  return "";
}
function resolveComments(node) {
  const content = node.content;
  if (content?.schemaVersion !== 1 || content.kind !== "blocks") return [];
  const comments = content.blocks.find((block) => block.type === "comments");
  if (!comments) return [];
  return comments.items.map((item) => ({ id: item.id, createdAt: item.createdAt, text: item.text }));
}
function resolveSummaryBodyText(summary) {
  const content = summary.content;
  if (content?.schemaVersion !== 1) return summary.text;
  if (content.kind === "plain-text") return content.text ?? "";
  if (content.kind === "richtext") {
    return extractPlainTextFromProseMirrorDoc(content.doc) || summary.text;
  }
  if (content.kind === "blocks") {
    const richtext = content.blocks.find((block) => block.type === "richtext");
    if (richtext && richtext.engine === "prosemirror") return extractPlainTextFromProseMirrorDoc(richtext.doc) || summary.text;
    return summary.text;
  }
  return summary.text;
}
function resolveSummaryNotesText(summary) {
  const content = summary.content;
  if (content?.schemaVersion !== 1 || content.kind !== "blocks") return null;
  const notes = content.blocks.find((block) => block.type === "notes");
  if (!notes) return null;
  const candidate = notes;
  if (typeof candidate.text === "string") return candidate.text;
  if (candidate.engine === "prosemirror" && candidate.doc && typeof candidate.doc === "object" && !Array.isArray(candidate.doc)) {
    return extractPlainTextFromProseMirrorDoc(candidate.doc);
  }
  return "";
}
function resolveSummaryComments(summary) {
  const content = summary.content;
  if (content?.schemaVersion !== 1 || content.kind !== "blocks") return [];
  const comments = content.blocks.find((block) => block.type === "comments");
  if (!comments) return [];
  return comments.items.map((item) => ({ id: item.id, createdAt: item.createdAt, text: item.text }));
}
function traverseNodeIdsInDoc(doc) {
  const result2 = [];
  const visited = /* @__PURE__ */ new Set();
  const walk = (nodeId) => {
    if (visited.has(nodeId)) return;
    visited.add(nodeId);
    result2.push(nodeId);
    const node = doc.nodes[nodeId];
    if (!node) return;
    for (const childId of node.children) walk(childId);
  };
  for (const rootId of doc.roots) walk(rootId);
  for (const id of Object.keys(doc.nodes)) {
    if (visited.has(id)) continue;
    walk(id);
  }
  return result2;
}
function searchInMindMapDocument(args) {
  const normalized = normalizeProjectSearchQuery(args.query);
  const trimmed = normalized.text.trim();
  if (!trimmed) return [];
  const fields = normalized.options.fields;
  const { matcher, error } = createMatcher(normalized);
  if (error) return [];
  const hits = [];
  for (const nodeId of traverseNodeIdsInDoc(args.doc)) {
    const node = args.doc.nodes[nodeId];
    if (!node) continue;
    const nodeTitle = String(node.text ?? "").trim() || nodeId;
    const entity = { kind: "node", id: nodeId, title: nodeTitle };
    if (fields.nodes) {
      const text = resolveNodeBodyText(node);
      const ranges = matcher.matchAll(text);
      if (ranges.length > 0) {
        hits.push({
          docId: args.docId,
          mapTitle: args.mapTitle,
          entity,
          field: "nodes",
          matchCount: ranges.length,
          snippet: buildSnippet(text, ranges)
        });
      }
    }
    if (fields.notes) {
      const notesText = resolveNotesText(node);
      if (notesText != null) {
        const ranges = matcher.matchAll(notesText);
        if (ranges.length > 0) {
          hits.push({
            docId: args.docId,
            mapTitle: args.mapTitle,
            entity,
            field: "notes",
            matchCount: ranges.length,
            snippet: buildSnippet(notesText, ranges)
          });
        }
      }
    }
    if (fields.comments) {
      for (const item of resolveComments(node)) {
        const ranges = matcher.matchAll(item.text);
        if (ranges.length === 0) continue;
        hits.push({
          docId: args.docId,
          mapTitle: args.mapTitle,
          entity,
          field: "comments",
          commentId: item.id,
          createdAt: item.createdAt,
          matchCount: ranges.length,
          snippet: buildSnippet(item.text, ranges)
        });
      }
    }
  }
  for (const summary of args.doc.summaries) {
    const summaryTitle = String(summary.text ?? "").trim() || summary.id;
    const entity = { kind: "summary", id: summary.id, title: summaryTitle };
    if (fields.nodes) {
      const text = resolveSummaryBodyText(summary);
      const ranges = matcher.matchAll(text);
      if (ranges.length > 0) {
        hits.push({
          docId: args.docId,
          mapTitle: args.mapTitle,
          entity,
          field: "nodes",
          matchCount: ranges.length,
          snippet: buildSnippet(text, ranges)
        });
      }
    }
    if (fields.notes) {
      const notesText = resolveSummaryNotesText(summary);
      if (notesText != null) {
        const ranges = matcher.matchAll(notesText);
        if (ranges.length > 0) {
          hits.push({
            docId: args.docId,
            mapTitle: args.mapTitle,
            entity,
            field: "notes",
            matchCount: ranges.length,
            snippet: buildSnippet(notesText, ranges)
          });
        }
      }
    }
    if (fields.comments) {
      for (const item of resolveSummaryComments(summary)) {
        const ranges = matcher.matchAll(item.text);
        if (ranges.length === 0) continue;
        hits.push({
          docId: args.docId,
          mapTitle: args.mapTitle,
          entity,
          field: "comments",
          commentId: item.id,
          createdAt: item.createdAt,
          matchCount: ranges.length,
          snippet: buildSnippet(item.text, ranges)
        });
      }
    }
  }
  return hits;
}
async function searchProjectV1(args) {
  const normalized = normalizeProjectSearchQuery(args.query);
  const trimmed = normalized.text.trim();
  if (!trimmed) return { hits: [], error: null, progress: { done: 0, total: 0, hits: 0 } };
  const { error } = createMatcher(normalized);
  if (error) return { hits: [], error, progress: { done: 0, total: 0, hits: 0 } };
  const maps = await collectProjectMapSummaries({ rootDocId: args.rootDocId, documents: args.documents, includeRoot: true });
  const total = maps.length;
  const hits = [];
  let done = 0;
  for (const map of maps) {
    if (args.signal?.aborted) break;
    const record = await args.documents.get(map.docId);
    done += 1;
    if (record) {
      hits.push(
        ...searchInMindMapDocument({
          docId: record.id,
          mapTitle: record.title || map.title || record.id,
          doc: record.doc,
          query: normalized
        })
      );
    }
    args.onProgress?.({ done, total, hits: hits.length });
  }
  return { hits, error: null, progress: { done, total, hits: hits.length } };
}

// ../app/src/services/import-debug.ts
init_src();

// src/services/load-project.ts
var textDecoder = new TextDecoder();
function decodeUtf82(bytes) {
  return textDecoder.decode(bytes);
}
function parseDocumentZipManifest(bytes) {
  const parsed = JSON.parse(decodeUtf82(bytes));
  if (parsed.schemaVersion !== 1) {
    throw new Error(`Unsupported document zip manifest version: ${String(parsed.schemaVersion ?? "")}`);
  }
  if (typeof parsed.rootDocId !== "string" || !parsed.rootDocId.trim()) {
    throw new Error("Invalid project file: missing rootDocId.");
  }
  if (!Array.isArray(parsed.documents)) {
    throw new Error("Invalid project file: missing documents list.");
  }
  return {
    schemaVersion: 1,
    rootDocId: parsed.rootDocId.trim(),
    documents: parsed.documents.map((item) => ({
      id: String(item?.id ?? "").trim(),
      title: String(item?.title ?? "").trim() || "Untitled",
      path: String(item?.path ?? "").trim()
    })).filter((item) => item.id && item.path)
  };
}
function buildRecord(args) {
  const meta = args.payload.header.documentsMeta[args.id];
  const now = Date.now();
  return {
    id: args.id,
    title: meta?.title ?? args.title ?? "Untitled",
    doc: args.doc,
    createdAt: meta?.createdAt ?? now,
    updatedAt: meta?.updatedAt ?? now,
    lastOpenedAt: meta?.lastOpenedAt ?? meta?.updatedAt ?? now
  };
}
function loadProjectFromSvgText(svgText) {
  const payload = parseKmindzProjectV3FromSvgText(svgText);
  if (!payload) {
    throw new Error("Invalid KMind project file: unsupported or missing kmindz v3 payload.");
  }
  const zipBytes = buildDocumentZipV1BytesFromKmindzProjectV3({ payload });
  const zipMap = readZipStore(zipBytes);
  const manifestBytes = zipMap.get("manifest.json");
  if (!manifestBytes) {
    throw new Error("Invalid project zip: missing manifest.json.");
  }
  const manifest = parseDocumentZipManifest(manifestBytes);
  const documents = manifest.documents.map((entry) => {
    const bytes = zipMap.get(entry.path);
    if (!bytes) {
      throw new Error(`Invalid project zip: missing document file: ${entry.path}`);
    }
    const doc = JSON.parse(decodeUtf82(bytes));
    const record = buildRecord({ id: entry.id, title: entry.title, doc, payload });
    return {
      id: record.id,
      title: record.title,
      path: entry.path,
      record
    };
  });
  const documentsById = new Map(documents.map((item) => [item.id, item]));
  const rootDocId = manifest.rootDocId;
  if (!documentsById.has(rootDocId)) {
    throw new Error(`Invalid project zip: missing root document: ${rootDocId}`);
  }
  return {
    payload,
    rootDocId,
    documents,
    documentsById,
    zipBytes
  };
}
function createLoadedProjectDocumentStore(project) {
  const map = new Map(project.documents.map((item) => [item.id, item.record]));
  return {
    async list() {
      return Array.from(map.values());
    },
    async get(id) {
      return map.get(id) ?? null;
    },
    async put(record) {
      map.set(record.id, record);
    },
    async delete(id) {
      map.delete(id);
    }
  };
}
function resolveLoadedProjectDocument(project, docIdRaw) {
  const normalized = String(docIdRaw ?? "").trim();
  const resolvedId = !normalized || normalized === "root" ? project.rootDocId : normalized;
  const document = project.documentsById.get(resolvedId);
  if (!document) {
    throw new Error(`Document not found: ${resolvedId}`);
  }
  return document;
}
function countDocumentAssets(doc) {
  return Object.keys(doc.assets ?? {}).length;
}
function summarizeLoadedProject(project) {
  const rootDocument = resolveLoadedProjectDocument(project, "root");
  return {
    schema: "kmind-cli-inspect@v1",
    rootDocId: project.rootDocId,
    title: rootDocument.title,
    revision: project.payload.header.rev,
    hostKind: typeof project.payload.header.host?.kind === "string" ? project.payload.header.host.kind : null,
    documentCount: project.documents.length,
    assetCount: project.payload.header.assetsManifest ? Object.keys(project.payload.header.assetsManifest).length : 0,
    documents: project.documents.map((item) => ({
      id: item.id,
      title: item.title,
      rootCount: item.record.doc.roots.length,
      nodeCount: Object.keys(item.record.doc.nodes ?? {}).length,
      summaryCount: Array.isArray(item.record.doc.summaries) ? item.record.doc.summaries.length : 0,
      relationCount: Array.isArray(item.record.doc.relations) ? item.record.doc.relations.length : 0,
      assetCount: countDocumentAssets(item.record.doc),
      createdAt: item.record.createdAt,
      updatedAt: item.record.updatedAt,
      lastOpenedAt: item.record.lastOpenedAt
    }))
  };
}

// src/utils/errors.ts
var CliUserError = class extends Error {
  exitCode;
  constructor(message, exitCode = 1) {
    super(message);
    this.name = "CliUserError";
    this.exitCode = exitCode;
  }
};
function formatCliError(error) {
  if (error instanceof CliUserError) {
    return { message: error.message, exitCode: error.exitCode };
  }
  if (error instanceof Error) {
    return { message: error.message || "Unknown CLI error.", exitCode: 1 };
  }
  return { message: "Unknown CLI error.", exitCode: 1 };
}

// src/utils/io.ts
import { mkdir, readFile, writeFile } from "node:fs/promises";
import path from "node:path";
async function readTextStream(stream) {
  const chunks = [];
  for await (const chunk of stream) {
    if (typeof chunk === "string") {
      chunks.push(Buffer.from(chunk));
      continue;
    }
    chunks.push(Buffer.from(chunk));
  }
  return Buffer.concat(chunks).toString("utf8");
}
async function readTextInput(args) {
  if (args.inputPath) {
    try {
      return await readFile(args.inputPath, "utf8");
    } catch (error) {
      const message = error instanceof Error ? error.message : `Failed to read file: ${args.inputPath}`;
      throw new CliUserError(message, 1);
    }
  }
  if (args.stdin.isTTY) {
    throw new CliUserError("Missing input path. Pass a Markdown file or pipe stdin.", 2);
  }
  return await readTextStream(args.stdin);
}
async function writeTextOutput(args) {
  const outputPath = String(args.outputPath ?? "").trim();
  if (!outputPath || outputPath === "-") {
    args.stdout.write(args.text);
    return;
  }
  const absolutePath = path.resolve(outputPath);
  await mkdir(path.dirname(absolutePath), { recursive: true });
  await writeFile(absolutePath, args.text, "utf8");
  args.stdout.write(`${absolutePath}
`);
}
async function writeBytesOutput(args) {
  const outputPath = String(args.outputPath ?? "").trim();
  if (!outputPath || outputPath === "-") {
    if (args.requireOutputPath) {
      throw new CliUserError("This format requires --output <path>.", 2);
    }
    args.stdout.write(Buffer.from(args.bytes));
    return;
  }
  const absolutePath = path.resolve(outputPath);
  await mkdir(path.dirname(absolutePath), { recursive: true });
  await writeFile(absolutePath, args.bytes);
  args.stdout.write(`${absolutePath}
`);
}

// src/commands/export.ts
function renderHelp() {
  return [
    "Usage:",
    "  kmind export <input> --format <format> [options]",
    "",
    "Options:",
    "  -o, --output <path>       Write result to file; otherwise print to stdout",
    "  --format <format>         Export format: json | markdown | docs-zip",
    "  --doc <id|root>          Export one document only (json/markdown)",
    "  -h, --help               Show command help"
  ].join("\n");
}
function normalizeFormat(value) {
  const format = String(value ?? "").trim().toLowerCase();
  if (format === "json" || format === "markdown" || format === "docs-zip") return format;
  throw new CliUserError("export requires --format json | markdown | docs-zip", 2);
}
function buildProjectJson(project, docIdRaw) {
  if (docIdRaw) {
    const document = resolveLoadedProjectDocument(project, docIdRaw);
    return {
      schema: "kmind-cli-document@v1",
      rootDocId: project.rootDocId,
      document: document.record
    };
  }
  return {
    schema: "kmind-cli-project@v1",
    rootDocId: project.rootDocId,
    header: project.payload.header,
    documents: project.documents.map((item) => item.record)
  };
}
function buildProjectMarkdown(project, docIdRaw) {
  if (docIdRaw) {
    const document = resolveLoadedProjectDocument(project, docIdRaw);
    return buildMindMapDocumentMarkdown(document.record.doc);
  }
  return project.documents.map((item) => {
    const body = buildMindMapDocumentMarkdown(item.record.doc).trim();
    return [`## ${item.title}`, "", body].join("\n");
  }).join("\n\n").trim() + "\n";
}
async function runExportCommand(args) {
  const parsed = parseArgs({
    args: args.argv,
    allowPositionals: true,
    options: {
      output: { type: "string", short: "o" },
      format: { type: "string" },
      doc: { type: "string" },
      help: { type: "boolean", short: "h" }
    }
  });
  if (parsed.values.help) {
    args.stdout.write(`${renderHelp()}
`);
    return;
  }
  if (parsed.positionals.length > 1) {
    throw new CliUserError("export accepts at most one input path.", 2);
  }
  const inputRaw = parsed.positionals[0] ?? "-";
  const inputPath = inputRaw === "-" ? null : inputRaw;
  const format = normalizeFormat(parsed.values.format);
  const text = await readTextInput({ inputPath, stdin: args.stdin });
  const project = loadProjectFromSvgText(text);
  if (format === "docs-zip") {
    await writeBytesOutput({
      outputPath: parsed.values.output,
      bytes: project.zipBytes,
      stdout: args.stdout,
      requireOutputPath: true
    });
    return;
  }
  const outputText = format === "json" ? `${JSON.stringify(buildProjectJson(project, parsed.values.doc), null, 2)}
` : buildProjectMarkdown(project, parsed.values.doc);
  await writeTextOutput({
    outputPath: parsed.values.output,
    text: outputText,
    stdout: args.stdout
  });
}

// src/commands/inspect.ts
import { parseArgs as parseArgs2 } from "node:util";
function renderHelp2() {
  return [
    "Usage:",
    "  kmind inspect <input> [options]",
    "",
    "Arguments:",
    "  <input>                   KMind project path, or '-' / omitted for stdin",
    "",
    "Options:",
    "  -o, --output <path>       Write result to file; otherwise print to stdout",
    "  --format <format>         Output format: json | text",
    "  -h, --help                Show command help"
  ].join("\n");
}
function normalizeFormat2(value) {
  const format = String(value ?? "json").trim().toLowerCase();
  if (format === "json" || format === "text") return format;
  throw new CliUserError(`Unsupported --format value: ${format}`, 2);
}
function renderText(summary) {
  return [
    `title: ${summary.title}`,
    `rootDocId: ${summary.rootDocId}`,
    `revision: ${summary.revision}`,
    `host: ${summary.hostKind ?? "-"}`,
    `documents: ${summary.documentCount}`,
    `assets: ${summary.assetCount}`,
    "",
    ...summary.documents.flatMap((item) => [
      `- ${item.title} (${item.id})`,
      `  roots=${item.rootCount} nodes=${item.nodeCount} summaries=${item.summaryCount} relations=${item.relationCount} assets=${item.assetCount}`
    ])
  ].join("\n");
}
async function runInspectCommand(args) {
  const parsed = parseArgs2({
    args: args.argv,
    allowPositionals: true,
    options: {
      output: { type: "string", short: "o" },
      format: { type: "string" },
      help: { type: "boolean", short: "h" }
    }
  });
  if (parsed.values.help) {
    args.stdout.write(`${renderHelp2()}
`);
    return;
  }
  if (parsed.positionals.length > 1) {
    throw new CliUserError("inspect accepts at most one input path.", 2);
  }
  const inputRaw = parsed.positionals[0] ?? "-";
  const inputPath = inputRaw === "-" ? null : inputRaw;
  const format = normalizeFormat2(parsed.values.format);
  const text = await readTextInput({ inputPath, stdin: args.stdin });
  const project = loadProjectFromSvgText(text);
  const summary = summarizeLoadedProject(project);
  const outputText = format === "json" ? `${JSON.stringify(summary, null, 2)}
` : `${renderText(summary)}
`;
  await writeTextOutput({
    outputPath: parsed.values.output,
    text: outputText,
    stdout: args.stdout
  });
}

// src/commands/import-markdown.ts
import { parseArgs as parseArgs3 } from "node:util";

// src/services/headless-project-svg.ts
import { createHash } from "node:crypto";
init_src();
var textEncoder = new TextEncoder();
function encodeUtf82(text) {
  return textEncoder.encode(text);
}
function sha256Hex(bytes) {
  return createHash("sha256").update(bytes).digest("hex");
}
function escapeXmlText2(value) {
  return value.replaceAll("&", "&amp;").replaceAll("<", "&lt;").replaceAll(">", "&gt;");
}
function sanitizeFileBaseName(value) {
  const trimmed = String(value ?? "").trim();
  const safe = trimmed.replace(/[\\/:*?"<>|]+/g, "_").replace(/\s+/g, " ").trim();
  return safe || "kmind";
}
function buildPreviewSvg(args) {
  const title = escapeXmlText2(args.title);
  const subtitle = escapeXmlText2(args.subtitle);
  return [
    '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 630" width="1200" height="630">',
    "  <defs>",
    '    <linearGradient id="kmind-cli-bg" x1="0" y1="0" x2="1" y2="1">',
    '      <stop offset="0%" stop-color="#f4efe7" />',
    '      <stop offset="100%" stop-color="#dbe7f3" />',
    "    </linearGradient>",
    "  </defs>",
    '  <rect width="1200" height="630" rx="32" fill="url(#kmind-cli-bg)" />',
    '  <rect x="64" y="64" width="1072" height="502" rx="28" fill="rgba(255,255,255,0.86)" stroke="rgba(15,23,42,0.08)" />',
    '  <text x="104" y="176" fill="#0f172a" font-size="56" font-weight="700" font-family="SF Pro Display, Helvetica, Arial, sans-serif">',
    `    ${title}`,
    "  </text>",
    '  <text x="104" y="236" fill="#475569" font-size="26" font-weight="500" font-family="SF Pro Text, Helvetica, Arial, sans-serif">',
    `    ${subtitle}`,
    "  </text>",
    '  <text x="104" y="516" fill="#64748b" font-size="24" font-family="SF Pro Text, Helvetica, Arial, sans-serif">',
    "    Generated by KMind CLI",
    "  </text>",
    "</svg>"
  ].join("\n");
}
function createHeadlessDocumentRecord(args) {
  const now = typeof args.now === "number" && Number.isFinite(args.now) ? args.now : Date.now();
  const title = String(args.title ?? "").trim() || "Untitled";
  return {
    id: args.id ?? createKmindId("doc", { now }),
    title,
    doc: args.doc,
    createdAt: now,
    updatedAt: now,
    lastOpenedAt: now
  };
}
function buildHeadlessProjectSvgText(args) {
  const rootDocId = String(args.rootDocId ?? "").trim();
  if (!rootDocId) {
    throw new Error("buildHeadlessProjectSvgText requires a rootDocId.");
  }
  const documents = args.documents.filter((item) => String(item.id ?? "").trim().length > 0);
  if (!documents.some((item) => item.id === rootDocId)) {
    throw new Error(`Root document not found: ${rootDocId}`);
  }
  const sortedDocuments = [...documents].sort((a, b) => a.id.localeCompare(b.id));
  const docsManifest = {
    schemaVersion: 1,
    rootDocId,
    documents: sortedDocuments.map((item) => ({
      id: item.id,
      title: item.title,
      path: `docs/${item.id}.json`
    }))
  };
  const docsZipBytes = createZipStore([
    { path: "manifest.json", bytes: encodeUtf82(JSON.stringify(docsManifest, null, 2)) },
    ...sortedDocuments.map((item) => ({
      path: `docs/${item.id}.json`,
      bytes: encodeUtf82(JSON.stringify(item.doc))
    }))
  ]);
  const docsHash = sha256Hex(docsZipBytes);
  const rootRecord = sortedDocuments.find((item) => item.id === rootDocId) ?? sortedDocuments[0];
  if (!rootRecord) {
    throw new Error("No documents available for export.");
  }
  const header = {
    format: "kmindz-project-svg",
    version: 3,
    mapKey: rootDocId,
    rootDocId,
    createdAt: rootRecord.createdAt,
    updatedAt: rootRecord.updatedAt,
    lastOpenedAt: rootRecord.lastOpenedAt,
    rev: docsHash,
    documentsMeta: Object.fromEntries(
      sortedDocuments.map((item) => [
        item.id,
        {
          id: item.id,
          title: item.title,
          createdAt: item.createdAt,
          updatedAt: item.updatedAt,
          lastOpenedAt: item.lastOpenedAt
        }
      ])
    ),
    hashes: { docs: docsHash },
    host: { kind: String(args.hostKind ?? "").trim() || "kmind-cli" }
  };
  const previewSvg = args.previewSvg ?? buildPreviewSvg({ title: rootRecord.title, subtitle: "KMind Zen (.kmindz.svg)" });
  return {
    svgText: encodeKmindzProjectV3IntoSvgText({
      previewSvg,
      header,
      docsZipB64: encodeBase64(docsZipBytes)
    }),
    safeTitle: sanitizeFileBaseName(rootRecord.title)
  };
}

// src/services/markdown-document.ts
import path2 from "node:path";
init_src();
var CLI_LAYOUT_OPTIONS = [
  "logical-right",
  "logical-left",
  "mindmap-both-auto"
];
var CLI_EDGE_ROUTE_OPTIONS = [
  "cubic",
  "edge-lead-quadratic",
  "center-quadratic",
  "orthogonal"
];
function deepClone3(value) {
  const clone = globalThis.structuredClone;
  if (typeof clone === "function") return clone(value);
  return JSON.parse(JSON.stringify(value));
}
function resolveFallbackTitle(args) {
  const explicit = String(args.explicitTitle ?? "").trim();
  if (explicit) return explicit;
  if (args.inputPath) {
    const parsed = path2.parse(args.inputPath);
    const base = parsed.name.trim();
    if (base) return base;
  }
  return "Imported Markdown";
}
function resolveThemeDefinitionFromPreset(themePresetId) {
  const requested = String(themePresetId ?? "").trim() || DEFAULT_THEME_PRESET_ID;
  const preset = resolveThemePreset(requested);
  if (!preset) {
    const known = THEME_PRESETS.map((item) => item.id).join(", ");
    throw new CliUserError(`Unknown --theme-preset value: ${requested}. Known presets: ${known}`, 2);
  }
  return {
    definition: deepClone3(preset.theme),
    presetId: preset.id
  };
}
function resolveRainbowEnabled(args) {
  if (args.rainbow === "on") return true;
  if (args.rainbow === "off") return false;
  return Boolean(args.definition.variants.light?.rainbow?.enabled || args.definition.variants.dark?.rainbow?.enabled);
}
function createThemeSummary(preset) {
  return {
    id: preset.id,
    name: preset.name,
    appVisible: preset.visibility?.app !== false,
    isDefault: preset.id === DEFAULT_THEME_PRESET_ID,
    lightEdgeRoute: preset.theme.variants.light?.edges?.routeType ?? "cubic",
    darkEdgeRoute: preset.theme.variants.dark?.edges?.routeType ?? preset.theme.variants.light?.edges?.routeType ?? "cubic",
    lightRainbowEnabled: Boolean(preset.theme.variants.light?.rainbow?.enabled),
    darkRainbowEnabled: Boolean(preset.theme.variants.dark?.rainbow?.enabled)
  };
}
function applyCliRootOptions(doc, args) {
  const rootId = doc.roots[0];
  if (!rootId) return doc;
  let nextDoc = doc;
  if (args.layout) {
    const rootNode = nextDoc.nodes[rootId];
    if (rootNode && rootNode.layout !== args.layout) {
      nextDoc = {
        ...nextDoc,
        nodes: {
          ...nextDoc.nodes,
          [rootId]: {
            ...rootNode,
            layout: args.layout
          }
        }
      };
    }
  }
  if (args.edgeRoute) {
    const theme = nextDoc.theme;
    if (theme) {
      nextDoc = {
        ...nextDoc,
        theme: {
          ...theme,
          rootEdgeRoutes: {
            ...theme.rootEdgeRoutes ?? {},
            [rootId]: args.edgeRoute
          }
        }
      };
    }
  }
  return nextDoc;
}
function normalizeCliRootLayout(value) {
  const normalized = String(value ?? "").trim().toLowerCase();
  if (!normalized) return void 0;
  if (CLI_LAYOUT_OPTIONS.includes(normalized)) {
    return normalized;
  }
  throw new CliUserError(`Unsupported --layout value: ${normalized}`, 2);
}
function normalizeCliEdgeRoute(value) {
  const normalized = String(value ?? "").trim().toLowerCase();
  if (!normalized) return void 0;
  if (CLI_EDGE_ROUTE_OPTIONS.includes(normalized)) {
    return normalized;
  }
  throw new CliUserError(`Unsupported --edge-route value: ${normalized}`, 2);
}
function listCliThemePresets() {
  return THEME_PRESETS.map(createThemeSummary);
}
function listCliRootLayouts() {
  return CLI_LAYOUT_OPTIONS.map((id) => ({ id }));
}
function listCliEdgeRoutes() {
  return CLI_EDGE_ROUTE_OPTIONS.map((id) => ({ id }));
}
function createCliDocumentFromMarkdown(args) {
  const fallbackTitle = resolveFallbackTitle({ inputPath: args.inputPath, explicitTitle: args.explicitTitle });
  const created = createDocumentFromMarkdownHeadings({
    markdown: args.markdown,
    fallbackRootText: fallbackTitle
  });
  if (!created.ok) {
    throw new CliUserError(created.error, 1);
  }
  const title = String(args.explicitTitle ?? "").trim() || created.rootText;
  const appearance = args.appearance ?? "light";
  const rainbow = args.rainbow ?? "auto";
  const { definition, presetId } = resolveThemeDefinitionFromPreset(args.themePresetId);
  const rainbowEnabled = resolveRainbowEnabled({ rainbow, definition });
  const themeState = createDefaultDocumentThemeState({
    source: "inline",
    value: definition
  });
  themeState.appearance = { mode: "fixed", fixed: appearance };
  themeState.rainbow = {
    enabled: rainbowEnabled,
    branchColors: {},
    paletteOverride: void 0
  };
  return {
    doc: applyCliRootOptions(
      {
        ...created.doc,
        theme: themeState
      },
      {
        layout: args.layout,
        edgeRoute: args.edgeRoute
      }
    ),
    title,
    rootText: created.rootText,
    appliedThemePresetId: presetId,
    appearance,
    rainbowEnabled
  };
}

// src/commands/import-markdown.ts
function renderHelp3() {
  return [
    "Usage:",
    "  kmind import-markdown <input> [options]",
    "",
    "Arguments:",
    "  <input>                   Markdown file path, or '-' / omitted for stdin",
    "",
    "Options:",
    "  -o, --output <path>       Write result to file; otherwise print to stdout",
    "  --format <format>         Output format: kmindz-svg | json",
    "  --title <title>           Override root document title",
    "  --theme-preset <id>       Built-in theme preset id (see: kmind themes)",
    `  --layout <id>            Root layout: ${CLI_LAYOUT_OPTIONS.join(" | ")}`,
    `  --edge-route <id>        Root branch route: ${CLI_EDGE_ROUTE_OPTIONS.join(" | ")}`,
    "  --appearance <mode>       Theme appearance: light | dark",
    "  --rainbow <mode>          Rainbow edges: auto | on | off",
    "  -h, --help                Show command help"
  ].join("\n");
}
function normalizeFormat3(value) {
  const format = String(value ?? "kmindz-svg").trim().toLowerCase();
  if (format === "kmindz-svg" || format === "json") return format;
  throw new CliUserError(`Unsupported --format value: ${format}`, 2);
}
function normalizeAppearance(value) {
  const appearance = String(value ?? "light").trim().toLowerCase();
  if (appearance === "light" || appearance === "dark") return appearance;
  throw new CliUserError(`Unsupported --appearance value: ${appearance}`, 2);
}
function normalizeRainbow(value) {
  const rainbow = String(value ?? "auto").trim().toLowerCase();
  if (rainbow === "auto" || rainbow === "on" || rainbow === "off") return rainbow;
  throw new CliUserError(`Unsupported --rainbow value: ${rainbow}`, 2);
}
async function runImportMarkdownCommand(args) {
  const parsed = parseArgs3({
    args: args.argv,
    allowPositionals: true,
    options: {
      output: { type: "string", short: "o" },
      format: { type: "string" },
      title: { type: "string" },
      "theme-preset": { type: "string" },
      layout: { type: "string" },
      "edge-route": { type: "string" },
      appearance: { type: "string" },
      rainbow: { type: "string" },
      help: { type: "boolean", short: "h" }
    }
  });
  if (parsed.values.help) {
    args.stdout.write(`${renderHelp3()}
`);
    return;
  }
  if (parsed.positionals.length > 1) {
    throw new CliUserError("import-markdown accepts at most one input path.", 2);
  }
  const inputRaw = parsed.positionals[0] ?? "-";
  const inputPath = inputRaw === "-" ? null : inputRaw;
  const format = normalizeFormat3(parsed.values.format);
  const markdown = await readTextInput({ inputPath, stdin: args.stdin });
  const created = createCliDocumentFromMarkdown({
    markdown,
    inputPath,
    explicitTitle: parsed.values.title,
    themePresetId: parsed.values["theme-preset"],
    layout: normalizeCliRootLayout(parsed.values.layout),
    edgeRoute: normalizeCliEdgeRoute(parsed.values["edge-route"]),
    appearance: normalizeAppearance(parsed.values.appearance),
    rainbow: normalizeRainbow(parsed.values.rainbow)
  });
  const record = createHeadlessDocumentRecord({
    doc: created.doc,
    title: created.title
  });
  const outputText = format === "json" ? `${JSON.stringify(record.doc, null, 2)}
` : `${buildHeadlessProjectSvgText({ rootDocId: record.id, documents: [record], hostKind: "kmind-cli" }).svgText}
`;
  await writeTextOutput({
    outputPath: parsed.values.output,
    text: outputText,
    stdout: args.stdout
  });
}

// src/commands/render-markdown.ts
import path5 from "node:path";
import { parseArgs as parseArgs4 } from "node:util";

// src/services/auto-browser.ts
import { spawn, spawnSync } from "node:child_process";
import { access, mkdtemp, rm } from "node:fs/promises";
import os from "node:os";
import path3 from "node:path";
async function pathExists(candidatePath) {
  try {
    await access(candidatePath);
    return true;
  } catch {
    return false;
  }
}
function resolveWhichCandidate(command) {
  const tool = process.platform === "win32" ? "where" : "which";
  const result2 = spawnSync(tool, [command], {
    encoding: "utf8",
    stdio: ["ignore", "pipe", "ignore"]
  });
  if (result2.status !== 0) return null;
  const output = String(result2.stdout ?? "").split(/\r?\n/g).map((line) => line.trim()).find(Boolean);
  return output ? path3.resolve(output) : null;
}
function getKnownBrowserCandidates() {
  const homeDir = os.homedir();
  if (process.platform === "darwin") {
    return [
      { label: "Google Chrome", executablePath: "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" },
      { label: "Google Chrome Canary", executablePath: "/Applications/Google Chrome Canary.app/Contents/MacOS/Google Chrome Canary" },
      { label: "Microsoft Edge", executablePath: "/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge" },
      { label: "Brave Browser", executablePath: "/Applications/Brave Browser.app/Contents/MacOS/Brave Browser" },
      { label: "Chromium", executablePath: "/Applications/Chromium.app/Contents/MacOS/Chromium" },
      { label: "Google Chrome (user)", executablePath: path3.join(homeDir, "Applications/Google Chrome.app/Contents/MacOS/Google Chrome") },
      { label: "Microsoft Edge (user)", executablePath: path3.join(homeDir, "Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge") },
      { label: "Brave Browser (user)", executablePath: path3.join(homeDir, "Applications/Brave Browser.app/Contents/MacOS/Brave Browser") }
    ];
  }
  if (process.platform === "win32") {
    const programFiles = process.env.PROGRAMFILES ?? "C:\\Program Files";
    const programFilesX86 = process.env["PROGRAMFILES(X86)"] ?? "C:\\Program Files (x86)";
    const localAppData = process.env.LOCALAPPDATA ?? path3.join(homeDir, "AppData", "Local");
    return [
      { label: "Google Chrome", executablePath: path3.join(programFiles, "Google/Chrome/Application/chrome.exe") },
      { label: "Google Chrome (x86)", executablePath: path3.join(programFilesX86, "Google/Chrome/Application/chrome.exe") },
      { label: "Microsoft Edge", executablePath: path3.join(programFiles, "Microsoft/Edge/Application/msedge.exe") },
      { label: "Microsoft Edge (x86)", executablePath: path3.join(programFilesX86, "Microsoft/Edge/Application/msedge.exe") },
      { label: "Brave Browser", executablePath: path3.join(programFiles, "BraveSoftware/Brave-Browser/Application/brave.exe") },
      { label: "Chromium", executablePath: path3.join(localAppData, "Chromium/Application/chrome.exe") }
    ];
  }
  return [
    { label: "google-chrome", executablePath: "/usr/bin/google-chrome" },
    { label: "chromium", executablePath: "/usr/bin/chromium" },
    { label: "chromium-browser", executablePath: "/usr/bin/chromium-browser" },
    { label: "microsoft-edge", executablePath: "/usr/bin/microsoft-edge" },
    { label: "brave-browser", executablePath: "/usr/bin/brave-browser" },
    { label: "google-chrome-stable", executablePath: "/usr/bin/google-chrome-stable" }
  ];
}
async function resolveRenderBrowserCandidate(explicitBrowserPath) {
  const envPath = String(process.env.KMIND_BROWSER_PATH ?? "").trim();
  const explicitPath = String(explicitBrowserPath ?? "").trim();
  const preferredPath = explicitPath || envPath;
  if (preferredPath) {
    const absolute = path3.resolve(preferredPath);
    if (!await pathExists(absolute)) {
      throw new CliUserError(`Browser executable not found: ${absolute}`, 2);
    }
    return { label: "explicit", executablePath: absolute };
  }
  for (const candidate of getKnownBrowserCandidates()) {
    if (await pathExists(candidate.executablePath)) {
      return candidate;
    }
  }
  for (const command of ["google-chrome", "google-chrome-stable", "chromium", "chromium-browser", "msedge", "microsoft-edge", "brave-browser", "brave"]) {
    const resolved = resolveWhichCandidate(command);
    if (resolved) {
      return { label: command, executablePath: resolved };
    }
  }
  return null;
}
function buildBrowserArgs(args) {
  const result2 = [
    `--user-data-dir=${args.userDataDir}`,
    "--no-first-run",
    "--no-default-browser-check",
    "--disable-default-apps",
    "--disable-background-networking",
    "--disable-sync",
    "--metrics-recording-only",
    "--hide-scrollbars",
    "--mute-audio",
    `--window-size=${args.viewport.width},${args.viewport.height}`
  ];
  if (!args.headed) {
    result2.push("--headless=new", "--disable-gpu");
  }
  result2.push(args.url);
  return result2;
}
function attachStderr(child, stderr) {
  if (!child.stderr) {
    return () => "";
  }
  const chunks = [];
  const stream = child.stderr;
  if ("setEncoding" in stream && typeof stream.setEncoding === "function") {
    stream.setEncoding("utf8");
  }
  stream.on("data", (chunk) => {
    const text = String(chunk);
    if (text.trim().length > 0) {
      stderr.write(`[kmind render browser] ${text}`);
    }
    chunks.push(text);
    if (chunks.length > 20) {
      chunks.splice(0, chunks.length - 20);
    }
  });
  return () => chunks.join("").trim();
}
async function launchRenderInLocalBrowser(args) {
  if (args.mode === "manual") return null;
  const candidate = await resolveRenderBrowserCandidate(args.browserPath);
  if (!candidate) {
    throw new CliUserError(
      "No supported local Chromium browser was found. Install Chrome / Edge / Brave / Chromium, or retry with --browser manual or --browser-path <path>.",
      1
    );
  }
  const userDataDir = await mkdtemp(path3.join(os.tmpdir(), "kmind-render-browser-"));
  const child = spawn(candidate.executablePath, buildBrowserArgs({
    headed: args.headed,
    viewport: args.viewport,
    userDataDir,
    url: args.url
  }), {
    stdio: ["ignore", "ignore", "pipe"]
  });
  const getStderrTail = attachStderr(child, args.stderr);
  let closed = false;
  const cleanup = async () => {
    if (!closed) {
      child.kill("SIGTERM");
    }
    await rm(userDataDir, { recursive: true, force: true });
  };
  const exited = new Promise((resolve, reject) => {
    child.once("error", async (error) => {
      closed = true;
      await rm(userDataDir, { recursive: true, force: true });
      reject(error);
    });
    child.once("close", async (code, signal) => {
      closed = true;
      const stderrTail = getStderrTail();
      await rm(userDataDir, { recursive: true, force: true });
      resolve({ code, signal, stderrTail });
    });
  });
  return {
    close: cleanup,
    exited
  };
}

// src/services/render-session.ts
import { mkdir as mkdir2, readFile as readFile2, writeFile as writeFile2 } from "node:fs/promises";
import { createServer } from "node:http";
import path4 from "node:path";
import { fileURLToPath } from "node:url";
function noStoreHeaders(extra = {}) {
  return {
    "cache-control": "no-store, no-cache, must-revalidate",
    pragma: "no-cache",
    expires: "0",
    ...extra
  };
}
function sendJson(res, statusCode, value) {
  const body = JSON.stringify(value, null, 2);
  res.writeHead(statusCode, noStoreHeaders({ "content-type": "application/json; charset=utf-8" }));
  res.end(body);
}
function sendText(res, statusCode, text, contentType = "text/plain; charset=utf-8") {
  res.writeHead(statusCode, noStoreHeaders({ "content-type": contentType }));
  res.end(text);
}
async function readRequestBytes(req) {
  const chunks = [];
  for await (const chunk of req) {
    if (typeof chunk === "string") {
      chunks.push(Buffer.from(chunk));
      continue;
    }
    chunks.push(Buffer.from(chunk));
  }
  return Buffer.concat(chunks);
}
async function closeServer(server) {
  await new Promise((resolve, reject) => {
    server.close((error) => {
      if (error) {
        reject(error);
        return;
      }
      resolve();
    });
  });
}
function buildHtmlPage() {
  return [
    "<!doctype html>",
    '<html lang="en">',
    "  <head>",
    '    <meta charset="utf-8" />',
    '    <meta name="viewport" content="width=device-width, initial-scale=1" />',
    "    <title>KMind Render Session</title>",
    "    <style>",
    "      :root { color-scheme: light dark; font-family: ui-sans-serif, system-ui, sans-serif; }",
    "      body { margin: 0; background: #f4f4f5; color: #18181b; }",
    "      .shell { min-height: 100vh; display: grid; grid-template-rows: auto 1fr; }",
    "      .status { padding: 16px 20px; border-bottom: 1px solid rgba(0,0,0,0.08); background: rgba(255,255,255,0.9); position: sticky; top: 0; backdrop-filter: blur(12px); }",
    "      .status code { font-size: 12px; }",
    "      #root { width: 100vw; height: calc(100vh - 65px); }",
    "    </style>",
    "  </head>",
    "  <body>",
    '    <div class="shell">',
    '      <div class="status">',
    "        <strong>KMind render session</strong>",
    '        <div id="status-text">Preparing render job\u2026</div>',
    "      </div>",
    '      <div id="root"></div>',
    "    </div>",
    '    <script type="module" src="/renderer.js"></script>',
    "  </body>",
    "</html>"
  ].join("\n");
}
function renderBrowserScriptPath() {
  const runtimeDir = path4.dirname(fileURLToPath(import.meta.url));
  return path4.join(runtimeDir, "render-job-browser.js");
}
async function startRenderSession(args) {
  const outputPath = path4.resolve(args.outputPath);
  const payload = args.payload;
  const rendererJs = await readFile2(renderBrowserScriptPath(), "utf8");
  const server = createServer();
  let settled = false;
  let settleResult = null;
  const donePromise = new Promise((resolve, reject) => {
    settleResult = (result2) => {
      if (settled) return;
      settled = true;
      if (result2.kind === "success") {
        resolve(result2.done);
        return;
      }
      reject(result2.error);
    };
  });
  const timeout = setTimeout(() => {
    settleResult?.({
      kind: "failure",
      error: new CliUserError(
        `Render session timed out after ${Math.round(args.timeoutMs / 1e3)}s. Open the printed URL in a local browser, or retry later.`,
        1
      )
    });
  }, args.timeoutMs);
  server.on("request", async (req, res) => {
    try {
      const requestUrl = new URL(req.url ?? "/", "http://127.0.0.1");
      if (req.method === "GET" && requestUrl.pathname === "/favicon.ico") {
        res.writeHead(204, noStoreHeaders());
        res.end();
        return;
      }
      if (req.method === "GET" && requestUrl.pathname === "/") {
        sendText(res, 200, buildHtmlPage(), "text/html; charset=utf-8");
        return;
      }
      if (req.method === "GET" && requestUrl.pathname === "/renderer.js") {
        sendText(res, 200, rendererJs, "text/javascript; charset=utf-8");
        return;
      }
      if (req.method === "GET" && requestUrl.pathname === "/job") {
        sendJson(res, 200, payload);
        return;
      }
      if (req.method === "POST" && requestUrl.pathname === "/result") {
        const bytes = await readRequestBytes(req);
        const mimeType = String(req.headers["content-type"] ?? "").trim() || (payload.format === "svg" ? "image/svg+xml" : "image/png");
        await mkdir2(path4.dirname(outputPath), { recursive: true });
        await writeFile2(outputPath, bytes);
        const done = {
          schema: "kmind-cli-render-session@v1",
          status: "done",
          format: payload.format,
          outputPath,
          byteLength: bytes.byteLength,
          mimeType
        };
        sendJson(res, 200, done);
        settleResult?.({ kind: "success", done });
        return;
      }
      if (req.method === "POST" && requestUrl.pathname === "/failure") {
        const bytes = await readRequestBytes(req);
        const message = Buffer.from(bytes).toString("utf8").trim() || "Browser render failed.";
        sendJson(res, 200, { ok: true });
        settleResult?.({ kind: "failure", error: new CliUserError(message, 1) });
        return;
      }
      sendText(res, 404, "Not found.");
    } catch (error) {
      const message = error instanceof Error ? error.message : "Unknown render session error.";
      sendText(res, 500, message);
      settleResult?.({ kind: "failure", error: new CliUserError(message, 1) });
    }
  });
  try {
    await new Promise((resolve, reject) => {
      server.listen(0, "127.0.0.1", () => resolve());
      server.on("error", reject);
    });
  } catch (error) {
    clearTimeout(timeout);
    if (server.listening) {
      await closeServer(server);
    }
    const detail = error instanceof Error ? error.message : "unknown listen error";
    throw new CliUserError(
      `Failed to start localhost render server: ${detail}. This command requires permission to listen on 127.0.0.1 and a local browser to open the session URL.`,
      1
    );
  }
  const address = server.address();
  if (!address || typeof address === "string") {
    clearTimeout(timeout);
    await closeServer(server);
    throw new CliUserError("Failed to start localhost render server.", 1);
  }
  const url = `http://127.0.0.1:${address.port}/`;
  const ready = {
    schema: "kmind-cli-render-session@v1",
    status: "ready",
    url,
    format: payload.format,
    outputPath,
    title: payload.title,
    message: "Open this URL in a local browser. The page will auto-render and save the output file."
  };
  const close = async () => {
    clearTimeout(timeout);
    if (server.listening) {
      await closeServer(server);
    }
  };
  void donePromise.finally(async () => {
    clearTimeout(timeout);
    if (server.listening) {
      await closeServer(server);
    }
  });
  return { ready, done: donePromise, close };
}

// src/commands/render-markdown.ts
function renderHelp4() {
  return [
    "Usage:",
    "  kmind render-markdown <input> --output <path> [options]",
    "",
    "Arguments:",
    "  <input>                      Markdown file path, or '-' / omitted for stdin",
    "",
    "Options:",
    "  -o, --output <path>          Output image path (.svg or .png)",
    "  --image-format <format>      Optional output format override: svg | png",
    "  --theme-preset <id>          Built-in theme preset id (see: kmind themes)",
    `  --layout <id>               Root layout: ${CLI_LAYOUT_OPTIONS.join(" | ")}`,
    `  --edge-route <id>           Root branch route: ${CLI_EDGE_ROUTE_OPTIONS.join(" | ")}`,
    "  --appearance <mode>          Theme appearance: light | dark",
    "  --rainbow <mode>             Rainbow edges: auto | on | off",
    "  --title <title>              Override root document title",
    "  --png-scale <number>         PNG export scale (default: 1)",
    "  --viewport-width <number>    Browser viewport width (default: 1600)",
    "  --viewport-height <number>   Browser viewport height (default: 900)",
    "  --timeout-ms <number>        Wait timeout for browser upload (default: 120000)",
    "  --browser <mode>             Browser mode: auto | manual (default: auto)",
    "  --browser-path <path>        Explicit local Chromium executable path",
    "  --browser-timeout-ms <n>     Browser navigation/render timeout (default: 30000)",
    "  --browser-headed             Launch a visible browser instead of headless",
    "  -h, --help                   Show command help",
    "",
    "Behavior:",
    "  This command starts a localhost render session and prints a ready JSON line.",
    "  If --image-format is omitted, the CLI infers svg/png from --output.",
    "  Export internals default to SVG=fidelity and PNG=accurate for webapp parity.",
    "  By default it tries to open a local Chromium browser automatically in headless mode.",
    "  Use --browser manual to keep the old workflow and open the printed URL yourself."
  ].join("\n");
}
function normalizeImageFormat(value) {
  const format = String(value ?? "svg").trim().toLowerCase();
  if (format === "svg" || format === "png") return format;
  throw new CliUserError(`Unsupported --image-format value: ${format}`, 2);
}
function inferImageFormatFromOutputPath(outputPath) {
  const ext = path5.extname(outputPath).trim().toLowerCase();
  if (ext === ".svg") return "svg";
  if (ext === ".png") return "png";
  return null;
}
function normalizeAppearance2(value) {
  const appearance = String(value ?? "light").trim().toLowerCase();
  if (appearance === "light" || appearance === "dark") return appearance;
  throw new CliUserError(`Unsupported --appearance value: ${appearance}`, 2);
}
function normalizeRainbow2(value) {
  const rainbow = String(value ?? "auto").trim().toLowerCase();
  if (rainbow === "auto" || rainbow === "on" || rainbow === "off") return rainbow;
  throw new CliUserError(`Unsupported --rainbow value: ${rainbow}`, 2);
}
function normalizeSvgMode(value) {
  const mode = String(value ?? "fidelity").trim().toLowerCase();
  if (mode === "fidelity" || mode === "portable") return mode;
  throw new CliUserError(`Unsupported --svg-mode value: ${mode}`, 2);
}
function normalizePngMode(value) {
  const mode = String(value ?? "accurate").trim().toLowerCase();
  if (mode === "fast" || mode === "accurate") return mode;
  throw new CliUserError(`Unsupported --png-mode value: ${mode}`, 2);
}
function normalizePositiveInt(value, fallback, optionName) {
  if (value == null || value === "") return fallback;
  const numberValue = Number(value);
  if (!Number.isFinite(numberValue) || numberValue <= 0) {
    throw new CliUserError(`${optionName} must be a positive number.`, 2);
  }
  return Math.round(numberValue);
}
function normalizeBrowserMode(value) {
  const mode = String(value ?? "auto").trim().toLowerCase();
  if (mode === "auto" || mode === "manual") return mode;
  throw new CliUserError(`Unsupported --browser value: ${mode}`, 2);
}
function normalizePngScale(value) {
  if (value == null || value === "") return 1;
  const scale = Number(value);
  if (!Number.isFinite(scale) || scale <= 0) {
    throw new CliUserError("--png-scale must be a positive number.", 2);
  }
  return Math.max(0.1, Math.min(6, Math.round(scale * 10) / 10));
}
async function runRenderMarkdownCommand(args) {
  const parsed = parseArgs4({
    args: args.argv,
    allowPositionals: true,
    options: {
      output: { type: "string", short: "o" },
      "image-format": { type: "string" },
      "theme-preset": { type: "string" },
      layout: { type: "string" },
      "edge-route": { type: "string" },
      appearance: { type: "string" },
      rainbow: { type: "string" },
      title: { type: "string" },
      "svg-mode": { type: "string" },
      "png-mode": { type: "string" },
      "png-scale": { type: "string" },
      "viewport-width": { type: "string" },
      "viewport-height": { type: "string" },
      "timeout-ms": { type: "string" },
      browser: { type: "string" },
      "browser-path": { type: "string" },
      "browser-timeout-ms": { type: "string" },
      "browser-headed": { type: "boolean" },
      help: { type: "boolean", short: "h" }
    }
  });
  if (parsed.values.help) {
    args.stdout.write(`${renderHelp4()}
`);
    return;
  }
  if (parsed.positionals.length > 1) {
    throw new CliUserError("render-markdown accepts at most one input path.", 2);
  }
  const outputPath = String(parsed.values.output ?? "").trim();
  if (!outputPath || outputPath === "-") {
    throw new CliUserError("render-markdown requires --output <path>.", 2);
  }
  const inputRaw = parsed.positionals[0] ?? "-";
  const inputPath = inputRaw === "-" ? null : inputRaw;
  const markdown = await readTextInput({ inputPath, stdin: args.stdin });
  const format = (() => {
    if (parsed.values["image-format"] != null && parsed.values["image-format"] !== "") {
      return normalizeImageFormat(parsed.values["image-format"]);
    }
    return inferImageFormatFromOutputPath(outputPath) ?? "svg";
  })();
  const browserMode = normalizeBrowserMode(parsed.values.browser);
  const browserTimeoutMs = normalizePositiveInt(parsed.values["browser-timeout-ms"], 3e4, "--browser-timeout-ms");
  void browserTimeoutMs;
  const browserPath = String(parsed.values["browser-path"] ?? "").trim() || void 0;
  const viewportWidth = normalizePositiveInt(parsed.values["viewport-width"], 1600, "--viewport-width");
  const viewportHeight = normalizePositiveInt(parsed.values["viewport-height"], 900, "--viewport-height");
  if (browserMode === "auto") {
    const candidate = await resolveRenderBrowserCandidate(browserPath);
    if (!candidate) {
      throw new CliUserError(
        "No supported local Chromium browser was found. Install Chrome / Edge / Brave / Chromium, or retry with --browser manual or --browser-path <path>.",
        1
      );
    }
    args.stderr.write(`Using local browser for headless render: ${candidate.executablePath}
`);
  }
  const docResult = createCliDocumentFromMarkdown({
    markdown,
    inputPath,
    explicitTitle: parsed.values.title,
    themePresetId: parsed.values["theme-preset"],
    layout: normalizeCliRootLayout(parsed.values.layout),
    edgeRoute: normalizeCliEdgeRoute(parsed.values["edge-route"]),
    appearance: normalizeAppearance2(parsed.values.appearance),
    rainbow: normalizeRainbow2(parsed.values.rainbow)
  });
  const session = await startRenderSession({
    outputPath,
    timeoutMs: normalizePositiveInt(parsed.values["timeout-ms"], 12e4, "--timeout-ms"),
    payload: {
      schema: "kmind-cli-render-job@v1",
      title: docResult.title,
      doc: docResult.doc,
      format,
      svgMode: normalizeSvgMode(parsed.values["svg-mode"]),
      pngMode: normalizePngMode(parsed.values["png-mode"]),
      pngScale: normalizePngScale(parsed.values["png-scale"]),
      viewport: {
        width: viewportWidth,
        height: viewportHeight
      }
    }
  });
  args.stdout.write(`${JSON.stringify(session.ready)}
`);
  let activeBrowser = null;
  try {
    if (browserMode === "auto") {
      args.stderr.write(`Auto-launching local browser for render session: ${session.ready.url}
`);
      activeBrowser = await launchRenderInLocalBrowser({
        url: session.ready.url,
        viewport: {
          width: viewportWidth,
          height: viewportHeight
        },
        mode: browserMode,
        browserPath,
        headed: Boolean(parsed.values["browser-headed"]),
        stderr: args.stderr
      });
    }
    const done = activeBrowser ? await Promise.race([
      session.done,
      activeBrowser.exited.then(async ({ code, signal, stderrTail }) => {
        await new Promise((resolve) => setTimeout(resolve, 200));
        const reason = code != null ? `exit code ${code}` : signal ? `signal ${signal}` : "unknown reason";
        const detail = stderrTail ? ` Browser stderr: ${stderrTail}` : "";
        throw new CliUserError(`Local browser exited before render completed (${reason}).${detail}`, 1);
      })
    ]) : await session.done;
    args.stdout.write(`${JSON.stringify(done)}
`);
  } finally {
    if (activeBrowser) {
      await activeBrowser.close();
    }
    await session.close();
  }
}

// src/commands/search.ts
import { parseArgs as parseArgs5 } from "node:util";
function renderHelp5() {
  return [
    "Usage:",
    "  kmind search <input> <query> [options]",
    "  kmind search <query> [options]     # when project content comes from stdin",
    "",
    "Options:",
    "  -o, --output <path>       Write result to file; otherwise print to stdout",
    "  --format <format>         Output format: json | text",
    "  --mode <mode>            Search mode: plain | regex | fuzzy",
    "  --fields <list>          Comma-separated fields: nodes,notes,comments",
    "  --case-sensitive         Enable case-sensitive matching",
    "  --whole-word             Enable whole-word matching",
    "  -h, --help               Show command help"
  ].join("\n");
}
function normalizeFormat4(value) {
  const format = String(value ?? "json").trim().toLowerCase();
  if (format === "json" || format === "text") return format;
  throw new CliUserError(`Unsupported --format value: ${format}`, 2);
}
function normalizeFields2(raw) {
  const value = String(raw ?? "").trim();
  if (!value) {
    return { nodes: true, notes: true, comments: true };
  }
  const allowed = /* @__PURE__ */ new Set(["nodes", "notes", "comments"]);
  const selected = new Set(
    value.split(",").map((item) => item.trim().toLowerCase()).filter(Boolean)
  );
  for (const entry of selected) {
    if (!allowed.has(entry)) {
      throw new CliUserError(`Unsupported field in --fields: ${entry}`, 2);
    }
  }
  return {
    nodes: selected.has("nodes"),
    notes: selected.has("notes"),
    comments: selected.has("comments")
  };
}
function resolveInputAndQuery(positionals) {
  if (positionals.length === 0) {
    throw new CliUserError("search requires a query.", 2);
  }
  if (positionals.length === 1) {
    return { inputPath: null, query: positionals[0] ?? "" };
  }
  if (positionals.length === 2) {
    const inputRaw = positionals[0] ?? "-";
    return {
      inputPath: inputRaw === "-" ? null : inputRaw,
      query: positionals[1] ?? ""
    };
  }
  throw new CliUserError("search accepts at most two positionals: <input> <query>.", 2);
}
function renderText2(result2) {
  if (result2.hits.length === 0) {
    return "No hits.";
  }
  return result2.hits.map((hit) => {
    const entityLabel = `${hit.entity.kind}:${hit.entity.title}`;
    return `[${hit.field}] ${hit.mapTitle} :: ${entityLabel} :: ${hit.snippet.text}`;
  }).join("\n");
}
async function runSearchCommand(args) {
  const parsed = parseArgs5({
    args: args.argv,
    allowPositionals: true,
    options: {
      output: { type: "string", short: "o" },
      format: { type: "string" },
      mode: { type: "string" },
      fields: { type: "string" },
      help: { type: "boolean", short: "h" },
      "case-sensitive": { type: "boolean" },
      "whole-word": { type: "boolean" }
    }
  });
  if (parsed.values.help) {
    args.stdout.write(`${renderHelp5()}
`);
    return;
  }
  const { inputPath, query } = resolveInputAndQuery(parsed.positionals);
  const format = normalizeFormat4(parsed.values.format);
  const text = await readTextInput({ inputPath, stdin: args.stdin });
  const project = loadProjectFromSvgText(text);
  const documents = createLoadedProjectDocumentStore(project);
  const normalizedQuery = normalizeProjectSearchQuery({
    text: query,
    options: {
      mode: parsed.values.mode,
      fields: normalizeFields2(parsed.values.fields),
      caseSensitive: parsed.values["case-sensitive"],
      wholeWord: parsed.values["whole-word"]
    }
  });
  const result2 = await searchProjectV1({
    rootDocId: project.rootDocId,
    documents,
    query: normalizedQuery
  });
  const payload = {
    schema: "kmind-cli-search@v1",
    rootDocId: project.rootDocId,
    query: normalizedQuery,
    result: result2
  };
  const outputText = format === "json" ? `${JSON.stringify(payload, null, 2)}
` : `${renderText2(result2)}
`;
  await writeTextOutput({
    outputPath: parsed.values.output,
    text: outputText,
    stdout: args.stdout
  });
}

// src/commands/themes.ts
import { parseArgs as parseArgs6 } from "node:util";
function renderHelp6() {
  return [
    "Usage:",
    "  kmind themes [options]",
    "",
    "List theme presets plus render layout and edge-route candidates.",
    "",
    "Options:",
    "  -o, --output <path>       Write result to file; otherwise print to stdout",
    "  --format <format>         Output format: json | text",
    "  -h, --help                Show command help"
  ].join("\n");
}
function normalizeFormat5(value) {
  const format = String(value ?? "json").trim().toLowerCase();
  if (format === "json" || format === "text") return format;
  throw new CliUserError(`Unsupported --format value: ${format}`, 2);
}
async function runThemesCommand(args) {
  const parsed = parseArgs6({
    args: args.argv,
    allowPositionals: true,
    options: {
      output: { type: "string", short: "o" },
      format: { type: "string" },
      help: { type: "boolean", short: "h" }
    }
  });
  if (parsed.values.help) {
    args.stdout.write(`${renderHelp6()}
`);
    return;
  }
  if (parsed.positionals.length > 0) {
    throw new CliUserError("themes does not accept positional arguments.", 2);
  }
  const presets = listCliThemePresets();
  const layouts = listCliRootLayouts();
  const edgeRoutes = listCliEdgeRoutes();
  const format = normalizeFormat5(parsed.values.format);
  const outputText = format === "json" ? `${JSON.stringify({ schema: "kmind-cli-themes@v1", presets, layouts, edgeRoutes }, null, 2)}
` : [
    "[themes]",
    ...presets.map(
      (preset) => `${preset.id}	${preset.name}	${preset.appVisible ? "app" : "hidden"}	default=${preset.isDefault ? "yes" : "no"}	route(light/dark)=${preset.lightEdgeRoute}/${preset.darkEdgeRoute}	rainbow(light/dark)=${preset.lightRainbowEnabled ? "on" : "off"}/${preset.darkRainbowEnabled ? "on" : "off"}`
    ),
    "",
    "[layouts]",
    ...layouts.map((item) => item.id),
    "",
    "[edge-routes]",
    ...edgeRoutes.map((item) => item.id),
    ""
  ].join("\n");
  await writeTextOutput({
    outputPath: parsed.values.output,
    text: outputText,
    stdout: args.stdout
  });
}

// src/run-cli.ts
function renderHelp7() {
  return [
    "KMind CLI",
    "",
    "Usage:",
    "  kmind <command> [options]",
    "",
    "Commands:",
    "  import-markdown <input>   Convert Markdown headings into a KMind project",
    "  inspect <input>           Read a KMind project and print structural summary",
    "  search <input> <query>    Search inside a KMind project",
    "  export <input>            Export a KMind project to json / markdown / docs-zip",
    "  themes                    List theme presets plus layout / edge-route options",
    "  render-markdown <input>   Render Markdown to SVG / PNG through a local browser session",
    "",
    "Global options:",
    "  -h, --help                Show help",
    "  -v, --version             Show version"
  ].join("\n");
}
function renderVersion() {
  return "0.0.0";
}
async function runCli(args) {
  try {
    const [command, ...rest] = args.argv;
    if (!command || command === "help" || command === "--help" || command === "-h") {
      args.stdout.write(`${renderHelp7()}
`);
      return { exitCode: 0 };
    }
    if (command === "version" || command === "--version" || command === "-v") {
      args.stdout.write(`${renderVersion()}
`);
      return { exitCode: 0 };
    }
    if (command === "import-markdown") {
      await runImportMarkdownCommand({ argv: rest, stdin: args.stdin, stdout: args.stdout });
      return { exitCode: 0 };
    }
    if (command === "inspect") {
      await runInspectCommand({ argv: rest, stdin: args.stdin, stdout: args.stdout });
      return { exitCode: 0 };
    }
    if (command === "search") {
      await runSearchCommand({ argv: rest, stdin: args.stdin, stdout: args.stdout });
      return { exitCode: 0 };
    }
    if (command === "export") {
      await runExportCommand({ argv: rest, stdin: args.stdin, stdout: args.stdout });
      return { exitCode: 0 };
    }
    if (command === "themes") {
      await runThemesCommand({ argv: rest, stdout: args.stdout });
      return { exitCode: 0 };
    }
    if (command === "render-markdown") {
      await runRenderMarkdownCommand({ argv: rest, stdin: args.stdin, stdout: args.stdout, stderr: args.stderr });
      return { exitCode: 0 };
    }
    throw new CliUserError(`Unknown command: ${command}`, 2);
  } catch (error) {
    const formatted = formatCliError(error);
    args.stderr.write(`${formatted.message}
`);
    return { exitCode: formatted.exitCode };
  }
}

// src/cli.ts
var result = await runCli({
  argv: process.argv.slice(2),
  stdin: process.stdin,
  stdout: process.stdout,
  stderr: process.stderr
});
if (result.exitCode !== 0) {
  process.exitCode = result.exitCode;
}
//# sourceMappingURL=cli.js.map
