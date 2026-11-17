#!/usr/bin/env Rscript
# ---------------------------------------------------------------------------
# Publication-ready enrichment dot plot (ggplot2)
#
# Default plotting engine for plot_enrichment.py.
#
#   Rscript plot_enrichment.R --input enrichment_all.tsv --output dotplot.png \
#       --source GO:BP --top 15 [--svg]
#
# Encodes: x = -log10(p), y = term (ordered by significance), bubble size =
# genes in term, bubble fill = significance on a blue -> red ramp.
# Outputs 300 dpi PNG plus an SVG with editable text.
# ---------------------------------------------------------------------------

suppressPackageStartupMessages({
  library(ggplot2)
  library(dplyr)
  library(stringr)
  library(scales)
})

# ---- shared look ----------------------------------------------------------
INK    <- "#222222"
MUTED  <- "#6B7280"
GRID   <- "#ECECEC"
SIG_RAMP <- c("#2C6BA8", "#4E9BD6", "#9FC9E8", "#F2E3B8", "#E9A03B", "#D2603A", "#B02418")

theme_pub <- function(base_size = 11) {
  theme_minimal(base_size = base_size, base_family = "sans") +
    theme(
      panel.grid.major.y = element_blank(),
      panel.grid.minor   = element_blank(),
      panel.grid.major.x = element_line(colour = GRID, linewidth = 0.35),
      axis.title.y       = element_blank(),
      axis.text.y        = element_text(colour = INK, size = base_size * 0.8),
      axis.text.x        = element_text(colour = MUTED, size = base_size * 0.78),
      axis.title.x       = element_text(colour = INK, size = base_size * 0.92),
      plot.title         = element_text(colour = "#111111", hjust = 0,
                                        size = base_size * 1.18, margin = margin(b = 2)),
      plot.subtitle      = element_text(colour = MUTED, hjust = 0,
                                        size = base_size * 0.78, margin = margin(b = 10)),
      legend.title       = element_text(colour = MUTED, size = base_size * 0.75),
      legend.text        = element_text(colour = MUTED, size = base_size * 0.7),
      legend.key.height  = unit(0.9, "lines"),
      plot.margin        = margin(14, 16, 10, 10)
    )
}

# ---- argument parsing -----------------------------------------------------
parse_args <- function(args) {
  out <- list(source = NULL, top = 15, color_by = NULL, wrap = 46,
              sort = "p", dpi = 300, width = NULL, height = NULL,
              title = NULL, svg = FALSE, input = NULL, output = NULL,
              p_cutoff = 0.05)
  i <- 1
  while (i <= length(args)) {
    a <- args[i]
    val <- if (i < length(args)) args[i + 1] else NA
    if (a == "--input")        { out$input <- val; i <- i + 2 }
    else if (a == "--output")  { out$output <- val; i <- i + 2 }
    else if (a == "--source")  { out$source <- val; i <- i + 2 }
    else if (a == "--top")     { out$top <- as.integer(val); i <- i + 2 }
    else if (a == "--color-by"){ out$color_by <- val; i <- i + 2 }
    else if (a == "--wrap")    { out$wrap <- as.integer(val); i <- i + 2 }
    else if (a == "--sort")    { out$sort <- val; i <- i + 2 }
    else if (a == "--dpi")     { out$dpi <- as.integer(val); i <- i + 2 }
    else if (a == "--width")   { out$width <- as.numeric(val); i <- i + 2 }
    else if (a == "--height")  { out$height <- as.numeric(val); i <- i + 2 }
    else if (a == "--title")   { out$title <- val; i <- i + 2 }
    else if (a == "--svg")     { out$svg <- TRUE; i <- i + 1 }
    else { i <- i + 1 }
  }
  out
}

opt <- parse_args(commandArgs(trailingOnly = TRUE))
if (is.null(opt$input) || is.null(opt$output)) {
  stop("Usage: plot_enrichment.R --input <tsv> --output <png> [--source GO:BP] [--top 15] [--svg]")
}
if (!file.exists(opt$input)) stop(sprintf("input file '%s' not found", opt$input))

df <- read.delim(opt$input, sep = "\t", check.names = FALSE, stringsAsFactors = FALSE)
if (!all(c("name", "p_value") %in% names(df))) {
  stop("input must contain 'name' and 'p_value' columns")
}

multi_source <- ("source" %in% names(df)) && (length(unique(df$source)) > 1)
if (!is.null(opt$source)) {
  if (!"source" %in% names(df)) stop("--source given but input has no 'source' column")
  df <- df[df$source == opt$source, , drop = FALSE]
  if (nrow(df) == 0) stop(sprintf("no terms for source '%s'", opt$source))
}

size_col <- c("intersection_size", "query_size", "term_size")
size_col <- size_col[size_col %in% names(df)][1]
if (is.na(size_col)) { df$.size <- 1; size_col <- ".size" }

# colour scale: adjusted p-value when available, else raw p
if (is.null(opt$color_by)) {
  opt$color_by <- if ("q_value" %in% names(df)) "q_value" else "p_value"
}
if (!opt$color_by %in% names(df)) opt$color_by <- "p_value"
adj_label <- if (grepl("q|adj", opt$color_by)) "BH-adjusted p (q)" else "p-value"

df <- df[order(if (opt$sort == "size") -df[[size_col]] else df$p_value), , drop = FALSE]
df <- head(df, opt$top)
df$neg_log10_p <- -log10(df$p_value)

lab <- str_wrap(df$name, width = opt$wrap)
if (multi_source) lab <- paste0(lab, "  (", sub("GO:", "", df$source), ")")
df$label <- factor(lab, levels = rev(unique(lab)))

n_q <- if ("query_size" %in% names(df)) max(df$query_size, na.rm = TRUE) else NA
sub <- paste0(
  if (!is.null(opt$source)) opt$source else "all sources",
  if (!is.na(n_q)) sprintf(" · %d query genes", n_q) else "",
  sprintf(" · top %d by %s", nrow(df), if (opt$sort == "size") "gene count" else "p-value"))

size_breaks <- pretty(range(df[[size_col]], na.rm = TRUE), n = 3)
size_breaks <- size_breaks[size_breaks >= min(df[[size_col]]) & size_breaks <= max(df[[size_col]])]
size_breaks <- if (length(size_breaks) < 2) unique(round(range(df[[size_col]]))) else size_breaks

p <- ggplot(df, aes(x = .data$neg_log10_p, y = .data$label)) +
  geom_point(aes(size = .data[[size_col]], fill = .data$neg_log10_p),
             shape = 21, colour = "white", stroke = 0.7) +
  scale_fill_gradientn(colours = SIG_RAMP, name = expression(-log[10](italic(p)))) +
  scale_size_continuous(range = c(2.2, 10), breaks = size_breaks,
                        name = "Genes in term") +
  scale_x_continuous(expand = expansion(mult = c(0.02, 0.10))) +
  labs(title = if (is.null(opt$title)) paste0("Enrichment analysis", if (!is.null(opt$source)) paste0(" - ", opt$source) else "") else opt$title,
       subtitle = sub, x = expression(-log[10](italic(p)))) +
  guides(fill = guide_colourbar(order = 1, barwidth = unit(0.55, "lines"),
                                barheight = unit(4.2, "lines"), ticks.colour = MUTED),
         size = guide_legend(order = 2, override.aes = list(fill = "#C6CDD6", colour = "white"))) +
  theme_pub()

# a light guide line at p = 0.05 when it falls inside the plotted range
p05 <- -log10(opt$p_cutoff)
if (min(df$neg_log10_p) <= p05 && max(df$neg_log10_p) >= p05) {
  p <- p + geom_vline(xintercept = p05, linetype = "dashed",
                      colour = "#C9CCD1", linewidth = 0.4) +
    annotate("text", x = p05, y = nrow(df) + 0.55, label = "p = 0.05",
             hjust = -0.1, vjust = 0, size = 2.6, colour = MUTED)
}

w <- if (!is.null(opt$width)) opt$width else max(6.6, 0.085 * max(nchar(as.character(df$label))) * 1.05 + 4.6)
h <- if (!is.null(opt$height)) opt$height else max(3.2, 0.42 * nrow(df) + 1.7)

ggsave(opt$output, plot = p, width = w, height = h, dpi = opt$dpi,
       bg = "white", limitsize = FALSE)
if (isTRUE(opt$svg)) {
  svg_path <- sub("\\.[^.]*$", ".svg", opt$output)
  if (requireNamespace("svglite", quietly = TRUE)) {
    ggsave(svg_path, plot = p, width = w, height = h,
           device = svglite::svglite, bg = "white")
  } else {
    grDevices::svg(svg_path, width = w, height = h, bg = "white")
    print(p)
    grDevices::dev.off()
  }
  cat(sprintf("Vector version written to %s\n", svg_path))
}
cat(sprintf("Dot plot written to %s (%d terms)\n", opt$output, nrow(df)))
