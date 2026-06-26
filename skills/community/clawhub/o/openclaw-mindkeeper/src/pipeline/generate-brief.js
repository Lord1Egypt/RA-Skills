import { humanDate } from "../utils/dates.js";
import { generateRecommendations } from "./generate-recommendations.js";

export function generateBrief({ date, title, signals }) {
  const recommendations = generateRecommendations(signals);

  return {
    title,
    date,
    humanDate: humanDate(date),
    summary: {
      whatMattered: signals.highlights,
      decisions: signals.decisions,
      openLoops: signals.openLoops,
      recommendations,
    },
  };
}
