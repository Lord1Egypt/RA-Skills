import { unique } from "../utils/text.js";

export function mergeSources(sources) {
  const lines = unique(sources.flatMap((source) => source.lines ?? []));

  return {
    sources: sources.map((source) => source.source),
    lines,
    raw: sources,
  };
}
