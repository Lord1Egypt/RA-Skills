// Characters refused in a path Codex might pass through a shell.
// The backtick is one of those characters. Kept in this small module as a normal literal.
export const SHELL_METACHAR = /[;|&`$<>\n\r()'"]/;
