import { readFile } from "node:fs/promises";

const SECTOR_REFERENCE_ROOT = new URL(
  "../../../references/research-flows/sector-analysis/",
  import.meta.url
);

const FLOW_CONTRACT_PATH = new URL(
  "../../../references/research-flows/sector-analysis/flow_contract.md",
  import.meta.url
);

const RUNTIME_PARITY_PATH = new URL(
  "../../../references/research-flows/runtime_parity.md",
  import.meta.url
);

const STEP_FILES = [
  ["step-0-macro", "modules/step-0-macro.md"],
  ["step-1-filter", "modules/step-1-filter.md"],
  ["step-2-classify", "modules/step-2-classify.md"],
  ["step-3-mining", "modules/step-3-mining.md"],
  ["step-4-thesis", "modules/step-4-thesis.md"],
  ["step-5-position", "modules/step-5-position.md"],
  ["step-6-risk", "modules/step-6-risk.md"],
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
  skill_name: "sector-analysis",
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
  const fileUrl = new URL(relativePath, SECTOR_REFERENCE_ROOT);
  const content = await readFile(fileUrl, "utf8");

  return {
    path: fileUrl.pathname,
    title: extractHeading(content)
  };
}

export async function loadSectorResearchReferences() {
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
