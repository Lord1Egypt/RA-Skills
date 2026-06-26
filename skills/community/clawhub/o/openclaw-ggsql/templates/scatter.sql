-- Scatter Plot Template
-- Required: x, y mapping
-- Optional: fill, color, shape, size

SELECT * FROM '{data_source}'
VISUALISE {x_column} AS x, {y_column} AS y
{#if fill_column}  , {fill_column} AS fill{/if}
{#if color_column}  , {color_column} AS color{/if}
{#if shape_column}  , {shape_column} AS shape{/if}
{#if size_column}  , {size_column} AS size{/if}
DRAW point
{#if scale_fill}SCALE {scale_fill} fill{/if}
{#if facet_column}FACET {facet_column}{/if}
LABEL
  title => '{title}',
  x => '{x_label}',
  y => '{y_label}'