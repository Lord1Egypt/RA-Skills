const { parsePage, parseDedao, parseIflyNote } = require('./parse.js');

const url = process.argv[2] || 'https://www.dedao.cn/share/packet?packetId=YDnPKqjEJz1xm3gDWTXaMilZxGQVelrO';

console.log('[INFO] Parsing URL:', url);
console.log('[INFO] Options: { saveImages: true, outputDir: "D:/notes/biji/0000/images" }\n');

parsePage(url, {
  saveImages: true,
  outputDir: 'D:/notes/biji/0000/images'
}).then(result => {
  if (result.success) {
    console.log('=== RESULT ===');
    console.log('Title:', result.title || '(none)');
    console.log('\nContent preview:', result.content.substring(0, 300) + '...');
    console.log('\nImages found:', result.images.length);
    result.images.forEach((img, i) => {
      console.log(`  ${i + 1}. ${img.originalUrl}`);
      console.log(`     Saved to: ${img.localPath}`);
    });
  } else {
    console.error('ERROR:', result.error);
  }
}).catch(err => {
  console.error('ERROR:', err.message);
});
