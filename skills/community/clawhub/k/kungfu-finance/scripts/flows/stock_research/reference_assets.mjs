import { readFile } from "node:fs/promises";

const STOCK_REFERENCE_ROOT = new URL(
  "../../../references/research-flows/stock-analysis/",
  import.meta.url
);

const FLOW_CONTRACT_PATH = new URL(
  "../../../references/research-flows/stock-analysis/flow_contract.md",
  import.meta.url
);

const RUNTIME_PARITY_PATH = new URL(
  "../../../references/research-flows/runtime_parity.md",
  import.meta.url
);

const STEP_FILES = [
  ["step-0-macro-sector", "modules/step-0-macro-sector.md"],
  ["step-1-company-profile", "modules/step-1-company-profile.md"],
  ["step-1b-forward-advantage", "modules/step-1b-forward-advantage.md"],
  ["step-2-financials", "modules/step-2-financials.md"],
  ["step-3-valuation", "modules/step-3-valuation.md"],
  ["step-4-price-action", "modules/step-4-price-action.md"],
  ["step-5-thesis", "modules/step-5-thesis.md"],
  ["step-6-catalyst", "modules/step-6-catalyst.md"],
  ["step-7a-skeptic", "modules/step-7a-skeptic.md"],
  ["step-7b-advocate", "modules/step-7b-advocate.md"],
  ["step-8-verdict", "modules/step-8-verdict.md"],
  ["step-9-output", "modules/step-9-output.md"]
];

const PROMPT_FILES = [
  "orchestrator_system.md",
  "worker_system.md",
  "synthesizer_notes.md"
];

const ORCHESTRATION_FILES = [
  "orchestration_contract.md",
  "shared_context_template.md"
];

const SOURCE_SKILL = {
  skill_name: "stock-analysis-v2",
  source_type: "external_codex_skill"
};

let cachedReferencesPromise;

function extractHeading(markdown) {
  const heading = markdown
    .split("\n")
    .map((line) => line.trim())
    .find((line) => /^#\s+/u.test(line));

  return heading ? heading.replace(/^#\s+/u, "").trim() : null;
}

async function loadMarkdownAsset(relativePath) {
  const fileUrl = new URL(relativePath, STOCK_REFERENCE_ROOT);
  const content = await readFile(fileUrl, "utf8");

  return {
    path: fileUrl.pathname,
    title: extractHeading(content)
  };
}

export async function loadStockResearchReferences() {
  if (!cachedReferencesPromise) {
    cachedReferencesPromise = (async () => {
      const [steps, promptAssets, orchestrationAssets] = await Promise.all([
        Promise.all(
          STEP_FILES.map(async ([step_id, relativePath]) => {
            const asset = await loadMarkdownAsset(relativePath);
            return {
              step_id,
              path: asset.path,
              title: asset.title
            };
          })
        ),
        Promise.all(
          PROMPT_FILES.map(async (relativePath) => {
            const asset = await loadMarkdownAsset(relativePath);
            return {
              path: asset.path,
              title: asset.title
            };
          })
        ),
        Promise.all(
          ORCHESTRATION_FILES.map(async (relativePath) => {
            const asset = await loadMarkdownAsset(relativePath);
            return {
              path: asset.path,
              title: asset.title
            };
          })
        )
      ]);

      return {
        source_skill: SOURCE_SKILL,
        flow_contract_path: FLOW_CONTRACT_PATH.pathname,
        runtime_parity_path: RUNTIME_PARITY_PATH.pathname,
        steps,
        prompt_assets: promptAssets,
        orchestration_assets: orchestrationAssets
      };
    })();
  }

  return cachedReferencesPromise;
}
