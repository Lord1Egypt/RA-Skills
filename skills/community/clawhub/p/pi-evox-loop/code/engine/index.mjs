/**
 * engine/index.mjs — 双后端统一接口
 *
 * 选择策略（0.12.0 起默认 light）：
 *   - 'light'（默认）→ 内置后端（纯 Node 内置模块，零 npm 依赖）；
 *   - 'evolver'      → 使用 node_modules 下的 evolver CLI（可选集成）；
 *   - 'auto'         → 旧行为：检测到 evolver 用 evolver，否则 light。
 *
 * 存储层（genes/review 读写）两后端共用同一实现（格式兼容 schema 1.13.0），
 * 因此产物可互操作：light 写入的基因，evolver 可直接读取（反之亦然）。
 */
import * as store from './light/store.mjs';
import * as lightDistill from './light/distill.mjs';
import * as lightLedger from './light/ledger.mjs';
import * as evolver from './evolver-bridge.mjs';

/**
 * @param {'auto'|'light'|'evolver'} preference
 * @param {{ root: string, log?: (s: string) => void }} ctx
 */
export function selectEngine(preference = 'light', { root, log = () => {} } = {}) {
  const evolverOk = evolver.available(root);
  let name;
  if (preference === 'evolver') {
    if (!evolverOk) throw new Error('指定 --engine evolver，但未找到 node_modules/@evomap/evolver（请先 npm install，或改用内置 light 后端）');
    name = 'evolver';
  } else if (preference === 'auto') {
    // 旧行为（0.11.x）：检测 evolver 则用 evolver
    name = evolverOk ? 'evolver' : 'light';
    log(`[engine] auto 选择后端：${name}（evolver ${evolverOk ? '可用' : '不可用'}）`);
  } else {
    // 0.12.0 起默认：内置 light 后端（零 npm 依赖）
    name = 'light';
  }

  const api = name === 'evolver'
    ? {
        name,
        ingestDistill: (transcriptPath) => {
          const r = evolver.ingestDistill(root, transcriptPath);
          return r;
        },
        distillManual: (opts) => evolver.distillManual(root, opts),
        approve: (geneId) => evolver.approve(root, geneId),
        injectBlock: () => evolver.injectSessionStart(root),
      }
    : {
        name,
        ingestDistill: (transcriptPath, disOpts = {}) => {
          const { gene, raw } = lightDistill.distillFromTranscript(transcriptPath, disOpts);
          if (!gene) return { geneId: null, raw }; // 无错误信号：不起草（对齐 evolver 语义）
          // 写入库并登记 quarantined（等价 evolver 的起草态）
          const written = store.appendGene(gene);
          store.appendReview({ assetId: gene.asset_id, state: 'quarantined', reason: 'auto-distilled — review before use' });
          return { geneId: gene.id, raw: written ? raw : `${raw}\n（asset 已存在，跳过重复写入）` };
        },
        distillManual: (opts) => {
          const { gene, raw } = lightDistill.distillManual(opts);
          const written = store.appendGene(gene);
          store.appendReview({ assetId: gene.asset_id, state: 'quarantined', reason: 'manually distilled — review before use' });
          return { geneId: gene.id, raw: written ? raw : `${raw}\n（asset 已存在，跳过重复写入）` };
        },
        approve: (geneId) => lightLedger.approve(geneId),
        // light 后端无演化标签块（evolver inject 输出的 summary 标签已知无信息量）；返回空串，由调用方拼装 strategy
        injectBlock: () => '',
      };

  return {
    ...api,
    // 存储与台账读取（两后端共用）
    readGenes: store.readGenes,
    readReview: store.readReview,
    approvedAssetIds: store.approvedAssetIds,
    assetIdOf: store.assetIdOf,
    ledgerList: lightLedger.list,
  };
}

export const storeApi = store;
