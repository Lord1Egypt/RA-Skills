#!/usr/bin/env Rscript
# ---------------------------------------------------------------------------
# Publication-ready conservation figures (ggplot2)
#
# Default plotting engine for conservation_analysis.py. Reads the tables that
# the Python analysis already wrote, so analysis and drawing stay separate.
#
#   Rscript plot_conservation.R --outdir results --prefix miR-21 \
#       --seed-start 2 --seed-end 8
#
# Needs: <prefix>_conservation.tsv and <prefix>_aligned.fa in --outdir.
# Writes <prefix>_sequence_logo.png/.svg and <prefix>_alignment.png/.svg
# ---------------------------------------------------------------------------

suppressPackageStartupMessages({
  library(ggplot2)
  library(dplyr)
})

BASE_COLORS <- c(A = "#2ecc71", C = "#3498db", G = "#f39c12", U = "#e74c3c")
INK   <- "#222222"
MUTED <- "#6B7280"
GRID  <- "#ECECEC"
SEED_TINT <- "#FBF0D5"

theme_pub <- function(base_size = 11) {
  theme_minimal(base_size = base_size, base_family = "sans") +
    theme(
      panel.grid.major = element_blank(),
      panel.grid.minor = element_blank(),
      axis.text.x  = element_text(colour = MUTED, size = base_size * 0.72),
      axis.text.y  = element_text(colour = INK,   size = base_size * 0.78),
      axis.title   = element_text(colour = INK,   size = base_size * 0.92),
      plot.title   = element_text(colour = "#111111", hjust = 0,
                                  size = base_size * 1.15, margin = margin(b = 8)),
      plot.margin  = margin(12, 14, 10, 10)
    )
}

parse_args <- function(args) {
  out <- list(outdir = ".", prefix = "conservation", seed_start = 2L,
              seed_end = 8L, dpi = 300, svg = TRUE)
  i <- 1
  while (i <= length(args)) {
    a <- args[i]; val <- if (i < length(args)) args[i + 1] else NA
    if (a == "--outdir")          { out$outdir <- val; i <- i + 2 }
    else if (a == "--prefix")     { out$prefix <- val; i <- i + 2 }
    else if (a == "--seed-start") { out$seed_start <- as.integer(val); i <- i + 2 }
    else if (a == "--seed-end")   { out$seed_end <- as.integer(val); i <- i + 2 }
    else if (a == "--dpi")        { out$dpi <- as.integer(val); i <- i + 2 }
    else if (a == "--no-svg")     { out$svg <- FALSE; i <- i + 1 }
    else { i <- i + 1 }
  }
  out
}

read_fasta <- function(path) {
  lines <- readLines(path, warn = FALSE)
  hdr <- which(startsWith(lines, ">"))
  if (!length(hdr)) return(data.frame(name = character(), seq = character()))
  ends <- c(hdr[-1] - 1, length(lines))
  data.frame(
    name = sub("^>", "", lines[hdr]),
    seq  = vapply(seq_along(hdr), function(k)
             paste(lines[(hdr[k] + 1):ends[k]], collapse = ""), character(1)),
    stringsAsFactors = FALSE)
}

save_plot <- function(p, path, w, h, dpi, svg) {
  ggsave(path, plot = p, width = w, height = h, dpi = dpi, bg = "white")
  if (isTRUE(svg)) {
    svg_path <- sub("\\.[^.]*$", ".svg", path)
    if (requireNamespace("svglite", quietly = TRUE)) {
      ggsave(svg_path, plot = p, width = w, height = h, device = svglite::svglite, bg = "white")
    } else {
      grDevices::svg(svg_path, width = w, height = h, bg = "white"); print(p); grDevices::dev.off()
    }
  }
}

opt <- parse_args(commandArgs(trailingOnly = TRUE))
cons_path <- file.path(opt$outdir, paste0(opt$prefix, "_conservation.tsv"))
aln_path  <- file.path(opt$outdir, paste0(opt$prefix, "_aligned.fa"))
if (!file.exists(cons_path)) stop(sprintf("missing %s", cons_path))

cons <- read.delim(cons_path, sep = "\t", check.names = FALSE, stringsAsFactors = FALSE)
cons$is_seed <- if ("is_seed" %in% names(cons)) cons$is_seed == "yes" else
  (cons$position >= opt$seed_start & cons$position <= opt$seed_end)

logo_range <- c(0, max(2.18, max(cons$bits, na.rm = TRUE) + 0.12))

seed_band <- if (any(cons$is_seed)) {
  geom_rect(data = data.frame(xmin = min(cons$position[cons$is_seed]) - 0.5,
                              xmax = max(cons$position[cons$is_seed]) + 0.5,
                              ymin = logo_range[1], ymax = logo_range[2]),
            aes(xmin = .data$xmin, xmax = .data$xmax,
                ymin = .data$ymin, ymax = .data$ymax),
            fill = SEED_TINT, alpha = 0.85, inherit.aes = FALSE)
} else NULL

# ---- 1. sequence logo -----------------------------------------------------
bases <- c("A", "C", "G", "U")
stack <- do.call(rbind, lapply(seq_len(nrow(cons)), function(i) {
  row <- cons[i, ]
  counts <- as.numeric(row[bases])
  valid <- sum(counts)
  if (valid == 0) return(NULL)
  coverage <- if ("coverage_percent" %in% names(cons)) as.numeric(row$coverage_percent) else 100
  bits <- as.numeric(row$bits)
  eff <- if (coverage >= 50) bits else bits * coverage / 100
  h <- (counts / valid) * eff
  order <- order(counts, decreasing = TRUE)
  bottom <- 0
  out <- lapply(order, function(k) {
    b <- bases[k]; hh <- h[k]
    seg <- data.frame(position = as.numeric(row$position), base = b,
                      ymin = bottom, ymax = bottom + hh, height = hh,
                      coverage = coverage, stringsAsFactors = FALSE)
    bottom <<- bottom + hh
    seg
  })
  do.call(rbind, out)
}))
stack <- stack[stack$height > 0.001, ]

logo <- ggplot(stack, aes(xmin = .data$position - 0.5, xmax = .data$position + 0.5,
                          ymin = .data$ymin, ymax = .data$ymax,
                          fill = .data$base)) +
  seed_band +
  geom_rect(colour = "white", linewidth = 0.35) +
  geom_text(data = subset(stack, height >= 0.24),
            aes(x = .data$position, y = (.data$ymin + .data$ymax) / 2, label = .data$base),
            size = 3.1, colour = "white", fontface = "bold", inherit.aes = FALSE) +
  scale_fill_manual(values = BASE_COLORS, guide = "none") +
  scale_x_continuous(breaks = pretty(cons$position, n = 8),
                     expand = expansion(mult = c(0.005, 0.005))) +
  scale_y_continuous(limits = logo_range, expand = expansion(mult = c(0, 0))) +
  labs(title = "miRNA sequence conservation",
       x = "Position (nt, 5\u2032 \u2192 3\u2032)", y = "Information content (bits)") +
  theme_pub() +
  theme(panel.grid.major.y = element_line(colour = GRID, linewidth = 0.3))
if (any(cons$is_seed)) {
  logo <- logo + geom_text(
    data = data.frame(x = mean(range(cons$position[cons$is_seed])),
                      y = max(logo_range) * 0.99,
                      lab = sprintf("seed (nt %d-%d)", min(cons$position[cons$is_seed]),
                                    max(cons$position[cons$is_seed]))),
    aes(x = .data$x, y = .data$y, label = .data$lab),
    size = 2.9, colour = "#9A7B3F", fontface = "italic", vjust = 1,
    hjust = 0.5, inherit.aes = FALSE)
}
save_plot(logo, file.path(opt$outdir, paste0(opt$prefix, "_sequence_logo.png")),
          max(6.5, nrow(cons) * 0.20), 3.1, opt$dpi, opt$svg)

# ---- 2. multiple sequence alignment --------------------------------------
if (file.exists(aln_path)) {
  fa <- read_fasta(aln_path)
  if (nrow(fa) > 0) {
    seqs <- strsplit(fa$seq, "", fixed = TRUE)
    width <- max(lengths(seqs))
    tiles <- do.call(rbind, lapply(seq_len(nrow(fa)), function(i) {
      s <- seqs[[i]]
      data.frame(row = i, name = fa$name[i], position = seq_along(s),
                 base = s, stringsAsFactors = FALSE)
    }))
    tiles$base[tiles$base == "-"] <- "gap"
    tiles$base[!(tiles$base %in% c("A", "C", "G", "U", "gap"))] <- "gap"
    pal <- c(BASE_COLORS, gap = "#E4E7EB")
    ymax_row <- nrow(fa)
    seed_band_aln <- if (any(cons$is_seed)) {
      geom_rect(data = data.frame(xmin = min(cons$position[cons$is_seed]) - 0.5,
                                  xmax = max(cons$position[cons$is_seed]) + 0.5,
                                  ymin = 0.5, ymax = ymax_row + 0.5),
                aes(xmin = .data$xmin, xmax = .data$xmax,
                    ymin = .data$ymin, ymax = .data$ymax),
                fill = SEED_TINT, alpha = 0.85, inherit.aes = FALSE)
    } else NULL
    aln <- ggplot(tiles, aes(x = .data$position, y = .data$row, fill = .data$base)) +
      seed_band_aln +
      geom_tile(colour = "white", linewidth = 0.3) +
      geom_text(data = subset(tiles, base != "gap"),
                aes(label = .data$base), size = 2.4, colour = "white",
                fontface = "bold", inherit.aes = TRUE) +
      scale_fill_manual(values = pal, guide = "none") +
      scale_x_continuous(breaks = pretty(1:width, n = 10),
                         expand = expansion(mult = c(0.005, 0.005))) +
      scale_y_reverse(breaks = seq_len(nrow(fa)), labels = fa$name,
                      expand = expansion(mult = c(0.01, 0.01))) +
      labs(title = sprintf("Multiple sequence alignment  (seed nt %d-%d highlighted)",
                           opt$seed_start, opt$seed_end),
           x = "Position (nt, 5\u2032 \u2192 3\u2032)", y = NULL) +
      theme_pub() +
      theme(panel.grid = element_blank())
    save_plot(aln, file.path(opt$outdir, paste0(opt$prefix, "_alignment.png")),
              max(6.5, width * 0.30), max(2.4, nrow(fa) * 0.40), opt$dpi, opt$svg)
  }
}

cat(sprintf("R conservation figures written to %s (%s_*)\n", opt$outdir, opt$prefix))
