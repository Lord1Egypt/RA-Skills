import { buildCommonRequest, isMain, parseCommonArgs, runCli } from "../core/cli.mjs";
import { assertMovementAnalysisEnabled } from "../core/rollout.mjs";
import { buildMovementBundle } from "../analysis/movement/bundle_builder.mjs";
import { buildMovementPromptPackage } from "../analysis/movement/prompt_builder.mjs";

export async function runMovementAnalysis(values) {
  assertMovementAnalysisEnabled();
  const request = buildCommonRequest(values);
  const bundle = await buildMovementBundle(request);
  const promptPackage = buildMovementPromptPackage(bundle);

  return {
    ...bundle,
    prompt_package: promptPackage
  };
}

if (isMain(import.meta)) {
  await runCli(async () => {
    const { values } = parseCommonArgs();
    return runMovementAnalysis(values);
  });
}
