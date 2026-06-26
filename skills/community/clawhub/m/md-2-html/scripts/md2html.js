// Markdown to HTML Converter
// Zero dependencies, Node.js v0.12+ compatible
// Usage: node md2html.js <input.md> [output.html]
//   Or:  node md2html.js - (reads stdin)
//   Or:  require('./md2html.js').markdownToHtml(mdString)

var fs = require('fs');

function markdownToHtml(md) {
  var lines = md.split('\n');
  var result = [];
  var inCodeBlock = false;
  var inList = false;
  var listType = '';

  for (var i = 0; i < lines.length; i++) {
    var line = lines[i];

    // Code blocks
    if (line.match(/^```/)) {
      if (inCodeBlock) {
        result.push('</code></pre>');
        inCodeBlock = false;
      } else {
        var lang = line.replace(/^```\s*/, '').trim();
        result.push('<pre><code' + (lang ? ' class="language-' + lang + '"' : '') + '>');
        inCodeBlock = true;
      }
      continue;
    }
    if (inCodeBlock) {
      result.push(escapeHtml(line));
      continue;
    }

    // Close list if next line is not a list item
    if (inList && !line.match(/^[\-\*]\s/) && !line.match(/^\d+\.\s/)) {
      result.push(listType === 'ol' ? '</ol>' : '</ul>');
      inList = false;
      listType = '';
    }

    // Headings (check from h6 to h1)
    if (line.match(/^######\s/)) {
      result.push('<h6>' + inlineFormat(line.replace(/^######\s*/, '')) + '</h6>');
    } else if (line.match(/^#####\s/)) {
      result.push('<h5>' + inlineFormat(line.replace(/^#####\s*/, '')) + '</h5>');
    } else if (line.match(/^####\s/)) {
      result.push('<h4>' + inlineFormat(line.replace(/^####\s*/, '')) + '</h4>');
    } else if (line.match(/^###\s/)) {
      result.push('<h3>' + inlineFormat(line.replace(/^###\s*/, '')) + '</h3>');
    } else if (line.match(/^##\s/)) {
      result.push('<h2>' + inlineFormat(line.replace(/^##\s*/, '')) + '</h2>');
    } else if (line.match(/^#\s/) && !line.match(/^#!\//)) {
      result.push('<h1>' + inlineFormat(line.replace(/^#\s*/, '')) + '</h1>');
    }
    // Blockquote
    else if (line.match(/^>\s/)) {
      result.push('<blockquote><p>' + inlineFormat(line.replace(/^>\s*/, '')) + '</p></blockquote>');
    }
    // Unordered list
    else if (line.match(/^[\-\*]\s/)) {
      if (!inList || listType !== 'ul') {
        if (inList) result.push(listType === 'ol' ? '</ol>' : '</ul>');
        result.push('<ul>');
        inList = true;
        listType = 'ul';
      }
      result.push('<li>' + inlineFormat(line.replace(/^[\-\*]\s*/, '')) + '</li>');
    }
    // Ordered list
    else if (line.match(/^\d+\.\s/)) {
      if (!inList || listType !== 'ol') {
        if (inList) result.push(listType === 'ol' ? '</ol>' : '</ul>');
        result.push('<ol>');
        inList = true;
        listType = 'ol';
      }
      result.push('<li>' + inlineFormat(line.replace(/^\d+\.\s*/, '')) + '</li>');
    }
    // Empty line
    else if (line.trim() === '') {
      result.push('');
    }
    // Horizontal rule
    else if (line.match(/^---+$/) || line.match(/^\*\*\*+$/)) {
      result.push('<hr>');
    }
    // Regular paragraph
    else {
      result.push('<p>' + inlineFormat(line) + '</p>');
    }
  }

  if (inList) result.push(listType === 'ol' ? '</ol>' : '</ul>');
  if (inCodeBlock) result.push('</code></pre>');

  return result.join('\n');
}

function inlineFormat(text) {
  // Images ![alt](url) — must come before links
  text = text.replace(/!\[(.+?)\]\((.+?)\)/g, '<img src="$2" alt="$1" style="max-width:100%;">');
  // Bold **text**
  text = text.replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>');
  // Italic *text* (Node v0.12+ compatible, no lookbehind needed)
  text = text.replace(/\*([^*\n]+?)\*/g, '<em>$1</em>');
  // Inline code `text`
  text = text.replace(/`(.+?)`/g, '<code>$1</code>');
  // Links [text](url)
  text = text.replace(/\[(.+?)\]\((.+?)\)/g, '<a href="$2" target="_blank" rel="noopener">$1</a>');
  // Line breaks (double space at end of line)
  text = text.replace(/  $/gm, '<br>');
  return text;
}

function escapeHtml(text) {
  return text.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
}

// Export for module usage
if (typeof module !== 'undefined' && module.exports) {
  module.exports = { markdownToHtml: markdownToHtml };
}

// CLI execution
if (require.main === module) {
  var input = process.argv[2];
  if (!input) {
    console.error('Usage: node md2html.js <input.md> [output.html]');
    console.error('       node md2html.js - (reads stdin)');
    process.exit(1);
  }

  var md, output;

  if (input === '-') {
    // Read from stdin
    var chunks = [];
    process.stdin.on('data', function(chunk) { chunks.push(chunk); });
    process.stdin.on('end', function() {
      md = Buffer.concat(chunks).toString('utf8');
      var html = markdownToHtml(md);
      process.stdout.write(html + '\n');
    });
  } else {
    // Read from file
    md = fs.readFileSync(input, 'utf8');
    output = process.argv[3] || input.replace(/\.(md|markdown)$/i, '.html');
    var html = markdownToHtml(md);
    fs.writeFileSync(output, html, 'utf8');
    console.log('Converted: ' + input + ' → ' + output);
  }
}