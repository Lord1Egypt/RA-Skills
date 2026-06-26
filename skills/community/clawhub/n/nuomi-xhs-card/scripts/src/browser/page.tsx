import React from 'react';
import { renderToStaticMarkup } from 'react-dom/server';

interface BrowserPageProps {
  styleText: string;
  bodyHtml: string;
}

function BrowserPage({ styleText, bodyHtml }: BrowserPageProps): React.ReactElement {
  return (
    <html lang="zh-CN">
      <head>
        <meta charSet="utf-8" />
        <meta name="viewport" content="width=device-width, initial-scale=1" />
        <style dangerouslySetInnerHTML={{ __html: styleText }} />
      </head>
      <body>
        <div id="app" dangerouslySetInnerHTML={{ __html: bodyHtml }} />
      </body>
    </html>
  );
}

export function renderBrowserPage(styleText: string, bodyHtml: string): string {
  return `<!doctype html>${renderToStaticMarkup(<BrowserPage styleText={styleText} bodyHtml={bodyHtml} />)}`;
}
