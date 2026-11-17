/**
 * industry-cycle-scrollytelling · pixel-font.js
 * 5-row pixel art font, variable width (3-5 cols).
 * 'X' = filled, '.' = empty.
 * Advance width = glyph[0].length + 1 (1-col space between glyphs).
 *
 * Origin: extracted from NVIDIA scrollytelling page (8 glyphs: R,T,X,N,V,I,D,A),
 *         extended to full A-Z + 0-9 + space/hyphen/period for any ticker.
 */
var FONT = {
  // —— Original 8 glyphs (kept verbatim for 1:1 NVIDIA regression) ——
  A:[".XX.","X..X","XXXX","X..X","X..X"],
  B:["XXX.","X..X","XXX.","X..X","XXX."],
  C:[".XXX","X...","X...","X...",".XXX"],
  D:["XX..","X.X.","X..X","X..X","XX.."],
  E:["XXXX","X...","XXX.","X...","XXXX"],
  F:["XXXX","X...","XXX.","X...","X..."],
  G:[".XXX","X...","X.XX","X..X",".XXX"],
  H:["X..X","X..X","XXXX","X..X","X..X"],
  I:["XXX",".X.",".X.",".X.","XXX"],
  J:["..XX","...X","...X","X..X",".XX."],
  K:["X..X","X.X.","XX..","X.X.","X..X"],
  L:["X...","X...","X...","X...","XXXX"],
  M:["X...X","XX.XX","X.X.X","X...X","X...X"],
  N:["X..X","XX.X","X.XX","X..X","X..X"],
  O:[".XX.","X..X","X..X","X..X",".XX."],
  P:["XXX.","X..X","XXX.","X...","X..."],
  Q:[".XX.","X..X","X..X","X.XX",".XXX"],
  R:["XX.","X.X","XX.","X.X","X.X"],
  S:[".XXX","X...",".XX.","...X","XXX."],
  T:["XXX",".X.",".X.",".X.",".X."],
  U:["X..X","X..X","X..X","X..X",".XX."],
  V:["X...X","X...X",".X.X.",".X.X.","..X.."],
  W:["X...X","X...X","X.X.X","XX.XX","X...X"],
  X:["X.X","X.X",".X.","X.X","X.X"],
  Y:["X...X",".X.X.","..X..","..X..","..X.."],
  Z:["XXXX","...X",".XX.","X...","XXXX"],
  // —— Digits ——
  "0":[".XX.","X..X","X..X","X..X",".XX."],
  "1":[".X..","XX..",".X..",".X..","XXX."],
  "2":["XXX.","...X",".XX.","X...","XXXX"],
  "3":["XXX.","...X",".XX.","...X","XXX."],
  "4":["X..X","X..X","XXXX","...X","...X"],
  "5":["XXXX","X...","XXX.","...X","XXX."],
  "6":[".XX.","X...","XXX.","X..X",".XX."],
  "7":["XXXX","...X","..X.",".X..",".X.."],
  "8":[".XX.","X..X",".XX.","X..X",".XX."],
  "9":[".XX.","X..X",".XXX","...X",".XX."],
  // —— Punctuation / space ——
  " ":["...","...","...","...","..."],
  "-":["...","...","XXX","...","..."],
  ".":["...","...","...","...",".X."],
  "/":["...X","..X.",".X..",".X..","X..."]
};
