// ============================================================
// KDP Book Template — Typst
// Amazon KDP-konform: Trim-Größen, Bleed, Gutter, Typografie
// Layout-Qualität: Hurenkinder/Waisen, sticky headings, recto-Kapitel
// ============================================================

#let trim-sizes = (
  "6x9":      (width: 6in,    height: 9in),
  "5.5x8.5":  (width: 5.5in,  height: 8.5in),
  "5x8":      (width: 5in,    height: 8in),
  "7x10":     (width: 7in,    height: 10in),
  "8.5x11":   (width: 8.5in,  height: 11in),
  "8.5x8.5":  (width: 8.5in,  height: 8.5in),
  "5.06x7.81":(width: 5.06in, height: 7.81in),
)

#let get-gutter(page-count-estimate) = {
  if page-count-estimate <= 150      { 0.375in }
  else if page-count-estimate <= 300 { 0.5in }
  else if page-count-estimate <= 500 { 0.625in }
  else if page-count-estimate <= 700 { 0.75in }
  else                               { 0.875in }
}

#let kdp-setup(
  title: "Buchtitel",
  author: "Autorenname",
  subtitle: none,
  language: "de",
  trim: "6x9",
  page-count-estimate: 200,
  bleed: false,
  body-font: "Inter",
  heading-font: "Inter",
  body-size: 11pt,
  line-height: 1.4,
  outside-margin: 0.5in,
  top-margin: 0.6in,
  bottom-margin: 0.7in,
  show-page-numbers: true,
  running-header: true,
  chapters-on-recto: true,
  isbn: none,
  doc,
) = {

  let trim-dim = trim-sizes.at(trim, default: trim-sizes.at("6x9"))
  let gutter = get-gutter(page-count-estimate)
  let bleed-size = if bleed { 0.125in } else { 0in }
  let page-width  = trim-dim.width  + bleed-size
  let page-height = trim-dim.height + (bleed-size * 2)
  let inner-margin = gutter
  let outer-margin = outside-margin

  set text(
    font: body-font,
    size: body-size,
    lang: language,
    hyphenate: true,
    costs: (
      widow:      100%,
      orphan:     100%,
      runt:        60%,
      hyphenation: 40%,
    ),
  )

  set par(
    justify: true,
    leading: line-height * body-size - body-size,
    first-line-indent: 0em,
    spacing: body-size * 1.4,
  )

  show raw.where(block: true): it => {
    v(0.3cm)
    block(
      width: 100%,
      fill: rgb("#0f172a"),
      stroke: (left: 3pt + rgb("#f59e0b")),
      inset: (left: 1em, right: 1em, top: 0.7em, bottom: 0.7em),
      breakable: false,
    )[
      #set text(font: "Liberation Mono", size: 9pt, fill: rgb("#e2e8f0"))
      #set par(justify: false, first-line-indent: 0em, leading: 0.4em)
      #it
    ]
    v(0.3cm)
  }

  show raw.where(block: false): it => {
    box(
      fill: rgb("#f1f5f9"),
      inset: (x: 4pt, y: 1pt),
      radius: 2pt,
    )[
      #set text(font: "Liberation Mono", size: 9.5pt, fill: rgb("#0f172a"))
      #it
    ]
  }

  set document(title: title, author: author)

  set page(
    width: page-width,
    height: page-height,
    margin: (
      inside:  inner-margin,
      outside: outer-margin,
      top:     top-margin,
      bottom:  bottom-margin,
    ),
    header: if running-header {
      context {
        let p = counter(page).get().first()
        let headings-on-page = query(heading.where(level: 1))
          .filter(h => h.location().page() == here().page())
        if p > 2 and headings-on-page.len() == 0 {
          set text(font: heading-font, size: 8pt, fill: rgb("#94a3b8"))
          set par(first-line-indent: 0em)
          stack(
            dir: ttb,
            if calc.odd(p) { align(right)[#title] }
            else           { align(left)[#title] },
            v(4pt),
            line(length: 100%, stroke: 0.5pt + rgb("#e2e8f0")),
          )
        }
      }
    },
    footer: if show-page-numbers {
      context {
        let p = counter(page).get().first()
        let headings-on-page = query(heading.where(level: 1))
          .filter(h => h.location().page() == here().page())
        if p > 2 and headings-on-page.len() == 0 {
          set text(size: 9pt)
          if calc.odd(p) { align(right)[#p] }
          else           { align(left)[#p] }
        }
      }
    },
  )

  show heading.where(level: 1): it => {
    page(
      width: page-width,
      height: page-height,
      margin: (top: 0pt, bottom: 0pt, left: 0pt, right: 0pt),
      header: none,
      footer: none,
    )[
      #v(1.8in)
      #rect(width: 100%, height: 6pt, fill: rgb("#f59e0b"))
      #pad(left: inner-margin, right: outer-margin)[
        #v(0.5in)
        #block[
          #set text(font: heading-font, size: 13pt, fill: rgb("#94a3b8"), tracking: 2pt)
          #set par(justify: false, first-line-indent: 0em)
          #upper[Kapitel #context counter(heading.where(level: 1)).display()]
        ]
        #v(14pt)
        #block[
          #set text(font: heading-font, size: 26pt, weight: "bold", fill: rgb("#d97706"))
          #set par(justify: false, first-line-indent: 0em, leading: 0.3em)
          #it.body
        ]
        #v(18pt)
        #rect(width: 60pt, height: 2pt, fill: rgb("#f59e0b"))
      ]
    ]
  }

  show heading.where(level: 2): it => {
    v(0.8cm)
    block(width: 100%, sticky: true)[
      #set text(font: heading-font, size: body-size * 1.25, weight: "bold")
      #set par(first-line-indent: 0em, justify: false)
      #it.body
    ]
    v(0.4cm)
  }

  show heading.where(level: 3): it => {
    v(0.5cm)
    block(width: 100%, sticky: true)[
      #set text(font: heading-font, size: body-size * 1.1, weight: "bold", style: "italic")
      #set par(first-line-indent: 0em, justify: false)
      #it.body
    ]
    v(0.25cm)
  }

  // Titelseite
  page(margin: (x: 1.5in, y: 1.5in))[
    #v(1fr)
    #align(center)[
      #set text(font: heading-font)
      #text(size: 20pt, weight: "bold")[#title]
      #if subtitle != none {
        v(0.5cm)
        text(size: 16pt, style: "italic")[#subtitle]
      }
      #v(1.5cm)
      #line(length: 60%, stroke: 0.5pt)
      #v(0.8cm)
      #text(size: 14pt)[#author]
    ]
    #v(1fr)
  ]

  // Copyright-Seite
  page(margin: (x: 1.2in, y: 1in))[
    #v(1fr)
    #set text(size: 8.5pt)
    #set par(justify: false, first-line-indent: 0em)
    #align(left)[
      *#title* \
      #if subtitle != none [#subtitle \ ]
      #v(0.3cm)
      Von #author \
      #v(0.5cm)
      Copyright © 2026 #author \
      Alle Rechte vorbehalten. \
      #v(0.3cm)
      Kein Teil dieses Buches darf ohne schriftliche Genehmigung \
      des Autors reproduziert oder verwendet werden. \
      #v(0.5cm)
      Erstveröffentlichung: 2026 \
      #if isbn != none [ISBN: #isbn \ ]
      Printed in Germany \
    ]
  ]

  counter(page).update(1)
  doc
}

// --- Hilfsfunktionen ---

#let epigraph(body, source: none) = {
  v(0.5cm)
  block(width: 80%, inset: (left: 1.5em, right: 1em, top: 0.5em, bottom: 0.5em), breakable: false)[
    #set text(style: "italic", size: 10pt)
    #set par(justify: false, first-line-indent: 0em)
    #body
    #if source != none [
      #v(0.2cm)
      #align(right)[#set text(style: "normal", size: 9pt); — #source]
    ]
  ]
  v(0.5cm)
}

#let _hint-box(label, border-color, bg-color, label-color, content) = {
  v(0.4cm)
  block(
    width: 100%,
    stroke: (left: 3pt + rgb(border-color)),
    inset: (left: 1em, right: 1em, top: 0.6em, bottom: 0.6em),
    fill: rgb(bg-color),
    breakable: true,
    sticky: true,
  )[
    #block[
      #set text(weight: "bold", size: 10pt, fill: rgb(label-color))
      #set par(first-line-indent: 0em)
      #label
    ]
    #v(0.15cm)
    #set text(size: 10.5pt)
    #set par(first-line-indent: 0em)
    #content
  ]
  v(0.4cm)
}

#let box-tip(content)     = _hint-box("Tipp",     "#3b82f6", "#eff6ff", "#3b82f6", content)
#let box-warning(content) = _hint-box("Warnung",  "#ef4444", "#fef2f2", "#ef4444", content)
#let box-success(content) = _hint-box("Erledigt", "#10b981", "#f0fdf4", "#10b981", content)
#let box-note(content)    = _hint-box("Hinweis",  "#f59e0b", "#fffbeb", "#d97706", content)

#let infobox(title: none, content) = _hint-box(
  if title != none { title } else { "Hinweis" },
  "#f59e0b", "#fffbeb", "#d97706", content
)

#let chapter-intro(content) = {
  v(0.3cm)
  block(width: 90%, inset: (left: 1.5em), sticky: true)[
    #set text(style: "italic", size: 10.5pt)
    #set par(first-line-indent: 0em)
    #content
  ]
  v(0.5cm)
}

#let dedication(content) = {
  pagebreak(to: "odd", weak: true)
  v(1fr)
  align(center)[
    #set text(style: "italic", size: 11pt)
    #set par(justify: false, first-line-indent: 0em)
    #content
  ]
  v(1fr)
  pagebreak()
}

#let scene-break() = {
  v(0.5cm)
  align(center)[#text(size: 14pt)[⁂]]
  v(0.5cm)
}

#let soft-break()    = pagebreak(weak: true)
#let chapter-start() = pagebreak(to: "odd", weak: false)

#let qr-block(qr-img, label, url, hint: "Am PC oder Tablet siehst du das volle interaktive Dashboard.") = {
  v(0.4cm)
  block(breakable: false, width: 100%)[
    #set par(first-line-indent: 0em)
    #grid(
      columns: (3cm, 1fr),
      gutter: 0.8em,
      qr-img,
      align(horizon)[
        #set text(size: 9pt)
        #text(weight: "bold")[#label] \
        #text(style: "italic")[#url] \
        #text(size: 8pt, fill: rgb("#555555"))[#hint]
      ]
    )
  ]
  v(0.4cm)
}
