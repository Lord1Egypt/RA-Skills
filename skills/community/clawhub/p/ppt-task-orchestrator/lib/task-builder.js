const PRIORITY_ORDER = {
  P0: 0,
  P1: 1,
  P2: 2,
};

function normalizePriority(input) {
  const value = String(input || "P1").toUpperCase();
  return value in PRIORITY_ORDER ? value : "P1";
}

function normalizeEdit(edit, page, positionHint) {
  if (edit.op === "place_image") {
    return {
      op: "place_image",
      imagePath: edit.imagePath || "",
      layerName: edit.layerName || "",
      position: edit.position || "top",
      visible: edit.visible !== false,
      targetArtboard: edit.targetArtboard || "",
      confidence: Number(edit.confidence ?? page.confidence ?? 0.9),
      positionHint,
    };
  }
  return {
    layerName: edit.layerName,
    op: edit.op === "delete_text" ? "delete_text" : "replace_text",
    newText: edit.op === "delete_text" ? "" : String(edit.newText || ""),
    confidence: Number(edit.confidence ?? page.confidence ?? 0.9),
    positionHint,
  };
}

export function buildBatchPreviewTasks(params = {}) {
  const pages = Array.isArray(params.pages) ? params.pages : [];
  if (pages.length === 0) {
    return {
      ok: false,
      code: "E_PARSE_FAILED",
      message: "No parsed pages to build preview tasks.",
    };
  }

  const invalid = pages.filter(
    (page) =>
      !(page.sourcePsd || page.exactPath) ||
      !Array.isArray(page.edits) ||
      page.edits.length === 0 ||
      !page.pageId,
  );
  if (invalid.length === pages.length) {
    // All pages invalid — hard fail.
    const first = invalid[0];
    return {
      ok: false,
      code: "E_PARSE_FAILED",
      message: `Invalid page task at slide ${first.slideIndex}: missing sourcePsd/pageId/edits.`,
    };
  }

  const sortedPages = [...pages].sort((a, b) => {
    const pa = PRIORITY_ORDER[normalizePriority(a.priority)];
    const pb = PRIORITY_ORDER[normalizePriority(b.priority)];
    if (pa !== pb) return pa - pb;
    return Number(a.slideIndex || 0) - Number(b.slideIndex || 0);
  });

  // ── Setup vs. output page separation ────────────────────────────────────────
  // "Setup pages" have no specific artboardName — they carry shared baseline
  // modifications (e.g. logo placement) that must be applied before every
  // output task.  They do NOT produce deliverable PNGs on their own.
  // "Output pages" have artboardName set — each produces one deliverable PNG.
  //
  // When output pages exist, setup-page edits are prepended to every output
  // task's edit list so each output task starts from the same enriched baseline.
  // When NO output pages exist (e.g. a simple all-layer-sets job), all pages
  // are treated as output pages and the setup/merge logic is bypassed.
  const setupPages = sortedPages.filter((p) => !(p.outputSpec?.artboardName));
  const outputPages = sortedPages.filter((p) => p.outputSpec?.artboardName);
  const effectiveOutputPages = outputPages.length > 0 ? outputPages : sortedPages;
  // Raw edits from all setup pages, to be prepended to each output task's edits.
  const setupRawEdits = outputPages.length > 0 ? setupPages.flatMap((p) => p.edits || []) : [];

  const taskMetaById = new Map();
  const previewTasks = effectiveOutputPages.map((page, index) => {
    const taskId = page.pageId || `ppt-page-${Date.now()}-${index + 1}`;
    const positionHint = `slide:${page.slideIndex},pageId:${page.pageId},mode:${page.parseMode}`;

    // Prepend setup edits (shared baseline) before this page's own edits.
    const allRawEdits = [...setupRawEdits, ...page.edits];
    const edits = allRawEdits.map((edit) => normalizeEdit(edit, page, positionHint));

    const minConfidence = edits.reduce(
      (min, item) => Math.min(min, Number(item.confidence || 1)),
      1,
    );
    const outputSpec = page.outputSpec || {};
    const preview = {
      taskId,
      exactPath:
        page.exactPath || (String(page.sourcePsd || "").startsWith("/") ? page.sourcePsd : ""),
      fileHint: page.exactPath ? undefined : page.sourcePsd,
      edits,
      minConfidence,
      // Per-task artboard name: used to export only this artboard instead of all layer sets.
      artboardName: outputSpec.artboardName || "",
    };
    taskMetaById.set(taskId, {
      pageId: page.pageId,
      slideIndex: page.slideIndex,
      parseMode: page.parseMode,
      priority: normalizePriority(page.priority),
      outputSpec,
    });
    return preview;
  });

  return {
    ok: true,
    previewTasks,
    sortedPages: effectiveOutputPages,
    taskMetaById,
  };
}

export function deriveBatchExportSpec(pages = []) {
  const first = pages[0] || {};
  const output = first.outputSpec || {};
  return {
    format: "png",
    mode: output.mode === "single" ? "single" : "layer_sets",
    bundleZip: output.bundleZip !== false,
  };
}
