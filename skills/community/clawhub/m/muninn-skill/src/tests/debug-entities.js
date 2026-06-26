/**
 * Debug entity extraction
 */
var __spreadArray = (this && this.__spreadArray) || function (to, from, pack) {
    if (pack || arguments.length === 2) for (var i = 0, l = from.length, ar; i < l; i++) {
        if (ar || !(i in from)) {
            if (!ar) ar = Array.prototype.slice.call(from, 0, i);
            ar[i] = from[i];
        }
    }
    return to.concat(ar || Array.prototype.slice.call(from));
};
// Inline entity extractor (same as in storage/index.ts)
function extractEntitiesFromText(text) {
    var entities = [];
    var patterns = [
        'Phillip', 'KakāpōHiko', 'Kakāpō', 'Hiko',
        'Elev8Advisory', 'BrandForge', 'Muninn', 'OpenClaw',
        'Sammy Clemens', 'Charlie Babbage', 'Donna Paulsen',
        'Brisbane', 'Australia', 'React', 'Node.js', 'PostgreSQL',
        'SQLite', 'Ollama', 'Stripe'
    ];
    for (var _i = 0, patterns_1 = patterns; _i < patterns_1.length; _i++) {
        var p = patterns_1[_i];
        if (text.toLowerCase().includes(p.toLowerCase())) {
            entities.push(p);
        }
    }
    return __spreadArray([], new Set(entities), true);
}
var queries = [
    "Who are all the AI agents on Phillip's team?",
    "What projects is Phillip building?",
    "What default port does OpenClaw gateway use?",
];
console.log('🔍 Entity Extraction Debug\n');
for (var _i = 0, queries_1 = queries; _i < queries_1.length; _i++) {
    var q = queries_1[_i];
    var entities = extractEntitiesFromText(q);
    console.log("Query: \"".concat(q, "\""));
    console.log("Entities: [".concat(entities.join(', '), "]\n"));
}
