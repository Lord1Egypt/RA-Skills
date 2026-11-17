import assert from 'node:assert/strict';
import fs from 'node:fs/promises';
import os from 'node:os';
import path from 'node:path';
import test from 'node:test';
import {
  attachCaseContext,
  prepareCaseMaterials,
  publicCaseContext,
  queryWithCaseContext
} from '../scripts/case-materials.mjs';
import { runCommand } from '../scripts/legal-skill.mjs';

test('纯文本案件材料会被直接提取并形成可复用案情上下文', async t => {
  const directory = await fs.mkdtemp(path.join(os.tmpdir(), 'haolvshi-materials-'));
  t.after(() => fs.rm(directory, { recursive: true, force: true }));
  const filePath = path.join(directory, '事故经过.txt');
  await fs.writeFile(filePath, '事故发生在杭州，对方承担全部责任，伤者构成十级伤残。', 'utf8');

  const materials = await prepareCaseMaterials({ filePaths: [filePath] });
  const context = publicCaseContext(materials);

  assert.deepEqual(materials.unresolvedFiles, []);
  assert.match(context.text, /事故发生在杭州/);
  assert.equal(context.files[0].source, 'local_text');
  assert.match(queryWithCaseContext('交通事故赔偿', materials), /十级伤残/);

  const interaction = attachCaseContext({ type: 'question' }, context);
  assert.equal(interaction.caseContext.useBeforePresenting, true);
  assert.equal(interaction.caseContext.displayToUser, false);
});

test('PDF、Word和图片需要宿主提取时不会被静默忽略', async t => {
  const directory = await fs.mkdtemp(path.join(os.tmpdir(), 'haolvshi-binary-materials-'));
  t.after(() => fs.rm(directory, { recursive: true, force: true }));
  const pdfPath = path.join(directory, '判决书.pdf');
  const docxPath = path.join(directory, '证据清单.docx');
  const imagePath = path.join(directory, '票据.png');
  await Promise.all([
    fs.writeFile(pdfPath, 'PDF测试占位'),
    fs.writeFile(docxPath, 'DOCX测试占位'),
    fs.writeFile(imagePath, 'PNG测试占位')
  ]);

  const pending = await prepareCaseMaterials({ filePaths: [pdfPath, docxPath, imagePath] });
  assert.deepEqual(pending.unresolvedFiles.map(file => file.extension), ['.pdf', '.docx', '.png']);

  const extracted = await prepareCaseMaterials({
    filePaths: [pdfPath, docxPath, imagePath],
    extractedTexts: [
      { filePath: pdfPath, text: '法院认定被告尚欠借款十万元。' },
      { filePath: docxPath, text: '证据包括借条和银行转账记录。' },
      { filePath: imagePath, text: '医疗费票据金额为12000元。' }
    ]
  });

  assert.deepEqual(extracted.unresolvedFiles, []);
  assert.match(extracted.text, /尚欠借款十万元/);
  assert.match(extracted.text, /医疗费票据金额为12000元/);
  assert.ok(extracted.files.every(file => file.source === 'host_extracted'));
});

test('文书图片可以延后交给后端视觉提取且不要求重复转写', async t => {
  const directory = await fs.mkdtemp(path.join(os.tmpdir(), 'haolvshi-image-materials-'));
  t.after(() => fs.rm(directory, { recursive: true, force: true }));
  const imagePath = path.join(directory, '起诉材料.jpg');
  await fs.writeFile(imagePath, 'JPG测试占位');

  const materials = await prepareCaseMaterials(
    { imagePaths: [imagePath] },
    { deferredExtensions: ['.jpg', '.jpeg', '.png'] }
  );

  assert.deepEqual(materials.unresolvedFiles, []);
  assert.equal(materials.deferredFiles.length, 1);
  assert.equal(materials.files[0].source, 'backend_image');
});

test('统一案件材料命令返回的caseContext可直接传入后续工作流', async t => {
  const directory = await fs.mkdtemp(path.join(os.tmpdir(), 'haolvshi-command-materials-'));
  t.after(() => fs.rm(directory, { recursive: true, force: true }));
  const filePath = path.join(directory, '工资证明.txt');
  await fs.writeFile(filePath, '伤者事故前月平均工资为8500元。', 'utf8');

  const extracted = await runCommand('case-materials', {
    capability: 'calculator',
    filePaths: [filePath]
  }, {
    config: {},
    api: {},
    store: {}
  });
  assert.equal(extracted.stage, 'materials_ready');
  assert.match(extracted.data.caseContext.text, /月平均工资为8500元/);

  const reused = await prepareCaseMaterials({ caseContext: extracted.data.caseContext });
  assert.match(reused.text, /月平均工资为8500元/);
});
