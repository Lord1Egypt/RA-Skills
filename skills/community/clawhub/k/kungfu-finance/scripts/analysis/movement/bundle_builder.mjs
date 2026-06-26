import { getUnusualMovementContext } from "../../products/unusual_movement_context.mjs";

const DEFAULT_MOVEMENT_DAYS = 100;

export async function buildMovementBundle(input) {
  const request = {
    ...input,
    visual_days_len: input.visual_days_len ?? DEFAULT_MOVEMENT_DAYS,
    is_realtime: true
  };
  const context = await getUnusualMovementContext(request);

  if (context?.success === false) {
    throw new Error(context.message ?? "Failed to build unusual movement context.");
  }

  return {
    flow: "movement_analysis",
    ...context,
    request: {
      ...request,
      ...(context?.request ?? {})
    },
    unusual_movements: context?.unusual_movements ?? {},
    historical_reports: context?.historical_reports ?? []
  };
}
