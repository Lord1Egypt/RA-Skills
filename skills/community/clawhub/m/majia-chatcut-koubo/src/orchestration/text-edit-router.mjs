const DENIED = /(?:不要|别|不|不想|不需要|无需|禁止|without|do not|don't)(?:再)?\s*$/iu;
const SIGNALS = [
  ["caption-display", /(?:只改字幕|(?:修改|改|删除|删掉|隐藏|更正)字幕|caption[- ]only|edit captions)/giu],
  ["transcript-repair", /(?:修正转写|更正转写|(?:修正|修复|更正|改)识别错误|ASR.{0,8}(?:识别错|听错|错误)|repair transcript)/giu],
  ["speech-cut", /(?:剪掉这句|剪掉这段话|删除这句口播|删掉这句口播|cut this sentence)/giu],
  ["spoken-replacement", /(?:替换原声|修复口误原声|修正说错的|替换说错的|修复说错的|fix spoken mistake|replace spoken audio)/giu],
];

// Conservative recognition: ambiguous or mixed targets become a question, never a cut.
export function inferTextEdit(input) {
  const text = String(input ?? "");
  const targets = SIGNALS.filter(([, pattern]) => [...text.matchAll(pattern)].some((match) => !DENIED.test(text.slice(0, match.index)))).map(([target]) => target);
  if (targets.length === 0 && !/(?:改这里的文字|删掉这里的文字|把这里的文字删掉)/u.test(text)) return null;
  const target = targets.length === 1 ? targets[0] : "clarify";
  return {
    target,
    changesSpokenAudio: ["speech-cut", "spoken-replacement"].includes(target),
    preservesTiming: target !== "speech-cut",
    requiresExplicitApproval: target === "spoken-replacement",
  };
}
