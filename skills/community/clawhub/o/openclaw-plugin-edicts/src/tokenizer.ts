/**
 * Default tokenizer: approximates token count as characters / 4.
 * ~85-90% accurate for English text. Users can inject a real
 * tokenizer (e.g., tiktoken) via EdictStoreOptions.tokenizer.
 */
export function defaultTokenizer(text: string): number {
  if (text.length === 0) return 0;
  return Math.ceil(text.length / 4);
}
