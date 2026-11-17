#!/usr/bin/env node
// Offline I Ching cast: three coins six times (heads = 3, tails = 2), bottom line first.
// 6 = old yin (changing), 7 = young yang, 8 = young yin, 9 = old yang (changing).
import { randomInt } from 'node:crypto';

// [lines bottom-to-top (1 = yang), King Wen number, page slug, English name]
const HEX = [
  ['111111', 1, '1-qian', 'The Creative'],
  ['000000', 2, '2-kun', 'The Receptive'],
  ['100010', 3, '3-zhun', 'Difficulty at the Beginning'],
  ['010001', 4, '4-meng', 'Youthful Folly'],
  ['111010', 5, '5-xu', 'Waiting'],
  ['010111', 6, '6-song', 'Conflict'],
  ['010000', 7, '7-shi', 'The Army'],
  ['000010', 8, '8-bi', 'Holding Together'],
  ['111011', 9, '9-xiao-chu', 'The Taming Power of the Small'],
  ['110111', 10, '10-lu', 'Treading'],
  ['111000', 11, '11-tai', 'Peace'],
  ['000111', 12, '12-pi', 'Standstill'],
  ['101111', 13, '13-tong-ren', 'Fellowship'],
  ['111101', 14, '14-da-you', 'Great Possession'],
  ['001000', 15, '15-qian', 'Modesty'],
  ['000100', 16, '16-yu', 'Enthusiasm'],
  ['100110', 17, '17-sui', 'Following'],
  ['011001', 18, '18-gu', 'Repairing What Is Spoiled'],
  ['110000', 19, '19-lin', 'Approach'],
  ['000011', 20, '20-guan', 'Contemplation'],
  ['100101', 21, '21-shi-he', 'Biting Through'],
  ['101001', 22, '22-bi', 'Grace'],
  ['000001', 23, '23-bo', 'Splitting Apart'],
  ['100000', 24, '24-fu', 'Return'],
  ['100111', 25, '25-wu-wang', 'Innocence'],
  ['111001', 26, '26-da-chu', 'The Taming Power of the Great'],
  ['100001', 27, '27-yi', 'Nourishment'],
  ['011110', 28, '28-da-guo', 'Great Excess'],
  ['010010', 29, '29-kan', 'The Abysmal'],
  ['101101', 30, '30-li', 'The Clinging Fire'],
  ['001110', 31, '31-xian', 'Influence'],
  ['011100', 32, '32-heng', 'Duration'],
  ['001111', 33, '33-dun', 'Retreat'],
  ['111100', 34, '34-da-zhuang', 'Great Power'],
  ['000101', 35, '35-jin', 'Progress'],
  ['101000', 36, '36-ming-yi', 'Darkening of the Light'],
  ['101011', 37, '37-jia-ren', 'The Family'],
  ['110101', 38, '38-kui', 'Opposition'],
  ['001010', 39, '39-jian', 'Obstruction'],
  ['010100', 40, '40-jie', 'Deliverance'],
  ['110001', 41, '41-sun', 'Decrease'],
  ['100011', 42, '42-yi', 'Increase'],
  ['111110', 43, '43-guai', 'Breakthrough'],
  ['011111', 44, '44-gou', 'Coming to Meet'],
  ['000110', 45, '45-cui', 'Gathering Together'],
  ['011000', 46, '46-sheng', 'Pushing Upward'],
  ['010110', 47, '47-kun', 'Oppression'],
  ['011010', 48, '48-jing', 'The Well'],
  ['101110', 49, '49-ge', 'Revolution'],
  ['011101', 50, '50-ding', 'The Cauldron'],
  ['100100', 51, '51-zhen', 'The Arousing Thunder'],
  ['001001', 52, '52-gen', 'Keeping Still'],
  ['001011', 53, '53-jian', 'Gradual Progress'],
  ['110100', 54, '54-gui-mei', 'The Marrying Maiden'],
  ['101100', 55, '55-feng', 'Abundance'],
  ['001101', 56, '56-lu', 'The Wanderer'],
  ['011011', 57, '57-xun', 'The Gentle Wind'],
  ['110110', 58, '58-dui', 'The Joyous Lake'],
  ['010011', 59, '59-huan', 'Dispersion'],
  ['110010', 60, '60-jie', 'Limitation'],
  ['110011', 61, '61-zhong-fu', 'Inner Truth'],
  ['001100', 62, '62-xiao-guo', 'Small Excess'],
  ['101010', 63, '63-ji-ji', 'After Completion'],
  ['010101', 64, '64-wei-ji', 'Before Completion'],
];
const byLines = new Map(HEX.map((h) => [h[0], h]));
const values = Array.from({ length: 6 }, () => [0, 1, 2].reduce((s) => s + (randomInt(2) ? 3 : 2), 0));
const show = (h) => `${h[1]}. ${h[3]}  https://www.tarotoper.com/en/i-ching/hexagrams/${h[2]}`;
values.forEach((v, i) => console.log(`Line ${i + 1}: ${v}${v === 6 || v === 9 ? ' (changing)' : ''}`));
const primary = byLines.get(values.map((v) => (v === 7 || v === 9 ? 1 : 0)).join(''));
console.log(`Primary: ${show(primary)}`);
const changing = values.flatMap((v, i) => (v === 6 || v === 9 ? [i + 1] : []));
if (changing.length) {
  const relating = byLines.get(values.map((v) => (v === 6 || v === 7 ? 1 : 0)).join(''));
  console.log(`Changing lines: ${changing.join(', ')}`);
  console.log(`Relating: ${show(relating)}`);
} else console.log('No changing lines.');
