-- Line Chart Template
-- Required: x, y
-- Optional: color, linetype

SELECT * FROM '{data_source}'
VISUALISE {x_column} AS x, {y_column} AS y
{#if color_column}  , {color_column} AS color{/if}
{#if linetype_column}  , {linetype_column} AS linetype{/if}
DRAW line
{#if scale_color}SCALE {scale_color} color{/if}
{#if facet_column}FACET {facet_column}{/if}
LABEL
  title => '{title}',
  x => '{x_label}',
  y => '{y_label}'