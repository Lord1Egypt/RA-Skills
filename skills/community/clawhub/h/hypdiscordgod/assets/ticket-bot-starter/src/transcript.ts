export type TranscriptLine = {
  authorTag: string;
  createdAt: string;
  content: string;
};

export function renderTranscript(lines: TranscriptLine[]): string {
  return lines
    .map((line) => `[${line.createdAt}] ${line.authorTag}: ${line.content}`)
    .join('\n');
}
