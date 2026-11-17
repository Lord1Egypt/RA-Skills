#!/usr/bin/env node
/**
 * ZHC · run_noos.js —— wasm32-unknown-unknown（no_std）目标宿主运行器
 *
 * 用途：wasm32-unknown-unknown 无 WASI 运行时，I/O 由内核垫片 zhc_noos_impl.c 的自管缓冲区承担，
 *      本脚本负责实例化模块、驱动 main、取回缓冲区字节并按 UTF-8 输出。
 *
 * 用法：
 *   node run_noos.js <目标.wasm>
 *   node run_noos.js <目标.wasm> --hex       输出十六进制而非文本
 *   node run_noos.js <目标.wasm> --info      只打印导出信息，不执行
 *
 * 宿主契约（缺一即报错退出，不做降级）：
 *   memory          内存实例
 *   main            入口函数，返回整型退出码
 *   zhc_out_reset   清空输出缓冲区
 *   zhc_out_ptr     缓冲区起始地址（函数或 global 均可）
 *   zhc_out_len     缓冲区已写长度（函数或 global 均可）
 *   zhc_out_cap     缓冲区容量（函数或 global 均可）
 *
 * 退出码：0 正常；1 用法错误；2 契约缺项；3 实例化失败；其余为 main 返回值。
 */
'use strict';

const fs = require('fs');
const path = require('path');

const 必需导出 = ['memory', 'main', 'zhc_out_reset', 'zhc_out_ptr', 'zhc_out_len', 'zhc_out_cap'];

function 取值(v) {
  if (typeof v === 'function') return Number(v());
  if (v && typeof v === 'object' && 'value' in v) return Number(v.value);
  return Number(v);
}

function 失败(码, 消息) {
  process.stderr.write('[run_noos] ' + 消息 + '\n');
  process.exit(码);
}

function 主() {
  const 参数 = process.argv.slice(2);
  if (参数.length === 0) {
    失败(1, '用法：node run_noos.js <目标.wasm> [--hex|--info]');
  }
  const 目标 = path.resolve(参数[0]);
  const 十六进制 = 参数.includes('--hex');
  const 只看信息 = 参数.includes('--info');

  if (!fs.existsSync(目标)) 失败(1, '文件不存在：' + 目标);

  const 字节 = fs.readFileSync(目标);
  let 实例;
  try {
    实例 = new WebAssembly.Instance(new WebAssembly.Module(字节), {});
  } catch (e) {
    失败(3, '实例化失败：' + (e && e.message ? e.message : String(e)));
  }

  const 导出 = 实例.exports;
  const 缺 = 必需导出.filter((名) => !(名 in 导出));
  if (缺.length > 0) {
    失败(2, '宿主契约缺项：' + 缺.join('、') + '（该模块可能不是 wasm32-unknown-unknown 目标）');
  }

  if (只看信息) {
    const 行 = 必需导出.map((名) => {
      const t = typeof 导出[名];
      const 描述 = t === 'function' ? '函数' : t === 'object' && 导出[名] && 'value' in 导出[名] ? 'global' : t;
      return '  ' + 名.padEnd(16) + 描述;
    });
    process.stdout.write('[run_noos] ' + 目标 + '\n' + 行.join('\n') + '\n');
    process.stdout.write('[run_noos] 缓冲区容量 ' + 取值(导出.zhc_out_cap) + ' 字节\n');
    return 0;
  }

  导出.zhc_out_reset();

  let 码 = 0;
  try {
    码 = 导出.main() | 0;
  } catch (e) {
    const 长度 = Math.min(取值(导出.zhc_out_len), 取值(导出.zhc_out_cap));
    const 指针 = 取值(导出.zhc_out_ptr);
    const 已写 = Buffer.from(导出.memory.buffer, 指针, 长度).toString('utf8');
    if (已写) process.stdout.write(已写);
    process.stderr.write('[run_noos] 运行中断（main 抛出）：' + (e && e.message ? e.message : String(e)) + '\n');
    return typeof e === 'object' && e && e.zhc_exit_code ? e.zhc_exit_code : 5;
  }

  const 指针 = 取值(导出.zhc_out_ptr);
  const 容量 = 取值(导出.zhc_out_cap);
  const 长度 = Math.min(取值(导出.zhc_out_len), 容量);
  const 视图 = Buffer.from(导出.memory.buffer, 指针, 长度);
  const 文本 = 十六进制 ? 视图.toString('hex') : 视图.toString('utf8');

  if (文本.length > 0) process.stdout.write(文本);

  return 码 & 0xff;
}

process.exitCode = 主();
