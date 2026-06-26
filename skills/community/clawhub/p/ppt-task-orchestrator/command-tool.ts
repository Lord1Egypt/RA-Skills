export type PptTaskPriority = "P0" | "P1" | "P2";

export type PptTaskParseMode = "structured" | "ocr_fallback";

export type PptTaskEditOp = "replace_text" | "delete_text";

export type PptTaskEditItem = {
  op: PptTaskEditOp;
  layerName: string;
  newText?: string;
  confidence?: number;
};

export type PptTaskPage = {
  slideIndex: number;
  pageId: string;
  sourcePsd?: string;
  exactPath?: string;
  edits: PptTaskEditItem[];
  outputSpec?: {
    format?: "png";
    mode?: "single" | "layer_sets";
    bundleZip?: boolean;
  };
  priority?: PptTaskPriority;
  note?: string;
  parseMode: PptTaskParseMode;
  confidence: number;
  screenshotPath?: string;
};

export type PptTaskOrchestratorRequest = {
  requestId?: string;
  pptPath: string;
  confidenceThreshold?: number;
  fallbackPolicy?: "structured_only" | "structured_first_with_ocr";
  execution?: {
    dryRun?: boolean;
    force?: boolean;
    indexPath?: string;
    rollbackPolicy?: "rollback_all";
    bundleZip?: boolean;
  };
  delivery?: {
    outputDir?: string;
    zipName?: string;
    copySelectedOnly?: boolean;
  };
};

export type PptTaskOrchestratorResult = {
  requestId: string;
  status: "success" | "error" | "dry-run" | "needs_confirmation";
  code: string;
  summary?: string;
  threshold: number;
  dryRun: boolean;
  forced: boolean;
  parsedPages: PptTaskPage[];
  executed?: Array<{
    pageId: string;
    slideIndex: number;
    taskId: string;
    status: "success" | "error";
    parseMode: PptTaskParseMode;
    resolvedPath?: string;
    psdOutputPath?: string;
    pngOutputPaths?: string[];
    selectedPngPath?: string;
    bundleZipPath?: string;
    code?: string;
    message?: string;
  }>;
  deliveryDir?: string;
  bundleZipPath?: string;
  failures?: Array<{
    pageId: string;
    slideIndex: number;
    code: string;
    message: string;
  }>;
  rolledBack?: boolean;
  rollbackCount?: number;
};
