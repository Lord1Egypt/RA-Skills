import React from 'react';
import { renderToStaticMarkup } from 'react-dom/server';
import { evaluate } from '@mdx-js/mdx';
import { Fragment, jsx, jsxs } from 'react/jsx-runtime';
import { unified } from 'unified';
import remarkParse from 'remark-parse';
import remarkGfm from 'remark-gfm';
import remarkRehype from 'remark-rehype';
import rehypeRaw from 'rehype-raw';
import rehypeStringify from 'rehype-stringify';

export interface MarkdownRenderOptions {
  mdxMode?: boolean;
}

export interface MarkdownRenderResult {
  html: string;
  warnings: string[];
}

async function mdxToHtml(markdown: string): Promise<string> {
  const mdxComponentNames = [...markdown.matchAll(/<([A-Z][A-Za-z0-9_]*)\b/g)].map((match) => match[1]);
  const fallbackComponents: Record<string, React.ComponentType<Record<string, unknown>>> = {};
  for (const componentName of mdxComponentNames) {
    if (fallbackComponents[componentName]) {
      continue;
    }
    fallbackComponents[componentName] = function UnknownMdxComponent(props: Record<string, unknown> = {}) {
      const { children } = props;
      return React.createElement(
        'div',
        {
          'data-mdx-component': componentName
        },
        children as React.ReactNode
      );
    };
  }

  const module = (await evaluate(markdown, {
    Fragment,
    jsx,
    jsxs,
    development: false,
    remarkPlugins: [remarkGfm]
  })) as { default: React.ComponentType<Record<string, unknown>> };

  const Component = module.default;
  const html = renderToStaticMarkup(
    React.createElement(Component, {
      components: fallbackComponents
    })
  ).trim();
  return html.length > 0 ? html : '<p><br></p>';
}

export async function markdownToHtml(markdown: string, options: MarkdownRenderOptions = {}): Promise<MarkdownRenderResult> {
  const warnings: string[] = [];

  if (options.mdxMode) {
    return {
      html: await mdxToHtml(markdown),
      warnings
    };
  }

  const file = await unified()
    .use(remarkParse)
    .use(remarkGfm)
    .use(remarkRehype, { allowDangerousHtml: true })
    .use(rehypeRaw)
    .use(rehypeStringify, { allowDangerousHtml: true })
    .process(markdown);

  const html = String(file.value).trim();
  return {
    html: html.length > 0 ? html : '<p><br></p>',
    warnings
  };
}
