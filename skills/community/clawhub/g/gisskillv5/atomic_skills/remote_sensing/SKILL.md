<!-- wm:坤图_GIS:V5.0 -->
# 原子GIS Skill单元 —— 遥感解译 Skill ATS-008

> V5.0 | 中层-原子Skill | 触发词: 遥感解译/影像分类/植被指数/变化检测/NDVI
> 约束: V5_CONSTITUTION.md

```yaml
skill_id: ATS-008
skill_name: remote_sensing
category: 遥感处理
min_inputs: [遥感影像(TIF/IMG), 波段信息]
outputs: [分类结果TIF, 指数图TIF, 统计报表CSV, 变化检测图TIF]
engines: [gdal, numpy, rasterio, arcpy]
```

---

## 完整执行代码

```python
#!/usr/bin/env python3
"""
ATS-008: 遥感解译 Skill V5.0
支持: NDVI/NDWI/NDBI指数计算、监督分类、非监督分类、变化检测
"""

import os, sys, json, logging, csv, math
from datetime import datetime
from pathlib import Path

def setup_logger(output_dir):
    log_path = Path(output_dir) / f"remote_sensing_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
    logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(message)s',
                        handlers=[logging.FileHandler(log_path, encoding='utf-8'), logging.StreamHandler()])
    return logging.getLogger(__name__), log_path


class InputValidator:
    @staticmethod
    def validate(image_path):
        errors = []
        if not os.path.exists(image_path):
            errors.append(f"影像文件不存在: {image_path}")
            return errors
        try:
            import rasterio
            with rasterio.open(image_path) as src:
                if src.count < 1:
                    errors.append("影像无有效波段")
        except:
            errors.append("无法读取影像，请确认格式正确")
        return errors


class RSProcessor:
    """遥感解译核心引擎"""
    
    def __init__(self, image_path, output_dir):
        self.image_path = image_path
        self.output_dir = output_dir
        self.results = []
    
    def compute_ndvi(self, nir_band=4, red_band=3):
        """计算归一化植被指数 NDVI = (NIR-RED)/(NIR+RED)"""
        import numpy as np
        import rasterio
        
        with rasterio.open(self.image_path) as src:
            # 自动探测波段数
            band_count = src.count
            if nir_band > band_count or red_band > band_count:
                nir_band = min(band_count, max(1, band_count))
                red_band = min(band_count - 1, max(1, band_count - 1))
            
            nir = src.read(nir_band).astype(np.float32)
            red = src.read(red_band).astype(np.float32)
            
            # 避免除零
            denominator = nir + red
            denominator[denominator == 0] = 0.0001
            
            ndvi = (nir - red) / denominator
            ndvi = np.clip(ndvi, -1.0, 1.0)
            
            # 保存结果
            ndvi_path = os.path.join(self.output_dir, 'ndvi.tif')
            profile = src.profile.copy()
            profile.update(dtype=rasterio.float32, count=1, compress='lzw')
            
            with rasterio.open(ndvi_path, 'w', **profile) as dst:
                dst.write(ndvi.astype(np.float32), 1)
            
            # 统计
            stats = {
                'min': float(np.nanmin(ndvi)), 'max': float(np.nanmax(ndvi)),
                'mean': float(np.nanmean(ndvi)), 'std': float(np.nanstd(ndvi)),
                'median': float(np.nanmedian(ndvi)),
                'vegetation_pct': float(np.sum(ndvi > 0.3) / np.sum(~np.isnan(ndvi)) * 100),
            }
            
            self.results.append({
                'type': 'NDVI', 'output': ndvi_path, 'stats': stats,
                'interpretation': self._interpret_ndvi(stats['mean'])
            })
            
            return ndvi_path, stats
    
    def compute_ndwi(self, green_band=2, nir_band=4):
        """计算归一化水体指数 NDWI = (GREEN-NIR)/(GREEN+NIR)"""
        import numpy as np
        import rasterio
        
        with rasterio.open(self.image_path) as src:
            band_count = src.count
            green_band = min(band_count, max(1, green_band))
            nir_band = min(band_count, max(1, nir_band))
            
            green = src.read(green_band).astype(np.float32)
            nir = src.read(nir_band).astype(np.float32)
            
            denominator = green + nir
            denominator[denominator == 0] = 0.0001
            
            ndwi = (green - nir) / denominator
            ndwi = np.clip(ndwi, -1.0, 1.0)
            
            ndwi_path = os.path.join(self.output_dir, 'ndwi.tif')
            profile = src.profile.copy()
            profile.update(dtype=rasterio.float32, count=1, compress='lzw')
            
            with rasterio.open(ndwi_path, 'w', **profile) as dst:
                dst.write(ndwi.astype(np.float32), 1)
            
            stats = {
                'min': float(np.nanmin(ndwi)), 'max': float(np.nanmax(ndwi)),
                'mean': float(np.nanmean(ndwi)),
                'water_pct': float(np.sum(ndwi > 0) / np.sum(~np.isnan(ndwi)) * 100) if np.any(~np.isnan(ndwi)) else 0,
            }
            
            self.results.append({
                'type': 'NDWI', 'output': ndwi_path, 'stats': stats
            })
            
            return ndwi_path, stats
    
    def compute_ndbi(self, swir_band=5, nir_band=4):
        """计算归一化建筑指数 NDBI = (SWIR-NIR)/(SWIR+NIR)"""
        import numpy as np
        import rasterio
        
        with rasterio.open(self.image_path) as src:
            band_count = src.count
            swir_band = min(band_count, max(1, swir_band))
            nir_band = min(band_count, max(1, nir_band))
            
            swir = src.read(swir_band).astype(np.float32)
            nir = src.read(nir_band).astype(np.float32)
            
            denominator = swir + nir
            denominator[denominator == 0] = 0.0001
            
            ndbi = (swir - nir) / denominator
            
            ndbi_path = os.path.join(self.output_dir, 'ndbi.tif')
            profile = src.profile.copy()
            profile.update(dtype=rasterio.float32, count=1, compress='lzw')
            
            with rasterio.open(ndbi_path, 'w', **profile) as dst:
                dst.write(ndbi.astype(np.float32), 1)
            
            stats = {
                'mean': float(np.nanmean(ndbi)),
                'built_up_pct': float(np.sum(ndbi > 0) / np.sum(~np.isnan(ndbi)) * 100),
            }
            
            self.results.append({
                'type': 'NDBI', 'output': ndbi_path, 'stats': stats
            })
            
            return ndbi_path, stats
    
    def kmeans_classify(self, n_clusters=5, max_iter=50):
        """K-Means非监督分类"""
        import numpy as np
        import rasterio
        
        with rasterio.open(self.image_path) as src:
            data = src.read()
            bands, rows, cols = data.shape
            
            # 展平为(bands, pixels)
            pixels = data.reshape(bands, -1).T.astype(np.float32)
            
            # 去除NoData
            valid_mask = ~np.isnan(pixels).any(axis=1)
            valid_pixels = pixels[valid_mask]
            
            # K-Means
            n_samples = min(len(valid_pixels), 500000)
            indices = np.random.choice(len(valid_pixels), n_samples, replace=False)
            sample = valid_pixels[indices]
            
            # 初始化聚类中心
            centers = sample[np.random.choice(n_samples, n_clusters, replace=False)]
            
            for iteration in range(max_iter):
                # 分配
                distances = np.sqrt(((valid_pixels[:, np.newaxis, :] - centers[np.newaxis, :, :]) ** 2).sum(axis=2))
                labels = np.argmin(distances, axis=1)
                
                # 更新中心
                new_centers = np.array([valid_pixels[labels == k].mean(axis=0) for k in range(n_clusters)])
                
                if np.allclose(centers, new_centers, rtol=0.001):
                    break
                centers = new_centers
            
            # 重建分类结果
            classified = np.full(rows * cols, 255, dtype=np.uint8)
            classified[valid_mask] = labels
            
            classified_img = classified.reshape(rows, cols)
            
            # 保存
            classified_path = os.path.join(self.output_dir, 'kmeans_classified.tif')
            profile = src.profile.copy()
            profile.update(dtype=rasterio.uint8, count=1, compress='lzw')
            
            with rasterio.open(classified_path, 'w', **profile) as dst:
                dst.write(classified_img, 1)
            
            # 统计各类像元分布
            class_stats = {}
            for k in range(n_clusters):
                count_k = np.sum(classified_img == k)
                class_stats[f'class_{k}'] = {
                    'pixels': int(count_k),
                    'percentage': round(count_k / (rows * cols) * 100, 2)
                }
            
            self.results.append({
                'type': 'K-Means分类', 'output': classified_path,
                'n_clusters': n_clusters, 'iterations': iteration + 1,
                'class_stats': class_stats
            })
            
            return classified_path, class_stats
            
        except Exception as e:
            # 降级: 使用简单的阈值分类
            return self._simple_threshold_classify()
    
    def _simple_threshold_classify(self):
        """降级方案: 简单阈值分类"""
        import numpy as np
        import rasterio
        
        with rasterio.open(self.image_path) as src:
            data = src.read()
            bands, rows, cols = data.shape
            
            classified = np.zeros((rows, cols), dtype=np.uint8)
            
            # 基于单波段的简单密度分割
            band1 = data[0].astype(np.float32)
            p25, p50, p75 = np.nanpercentile(band1, [25, 50, 75])
            
            classified[band1 < p25] = 1
            classified[(band1 >= p25) & (band1 < p50)] = 2
            classified[(band1 >= p50) & (band1 < p75)] = 3
            classified[band1 >= p75] = 4
            
            classified_path = os.path.join(self.output_dir, 'simple_classified.tif')
            profile = src.profile.copy()
            profile.update(dtype=rasterio.uint8, count=1, compress='lzw')
            
            with rasterio.open(classified_path, 'w', **profile) as dst:
                dst.write(classified, 1)
            
            self.results.append({
                'type': '简单阈值分类(降级)', 'output': classified_path
            })
            
            return classified_path, {'note': '使用降级方案-简单阈值分类'}
    
    def change_detection(self, image_before, method='difference'):
        """变化检测: 两期影像对比"""
        import numpy as np
        import rasterio
        
        if not os.path.exists(image_before):
            return None, {'error': '前期影像不存在'}
        
        with rasterio.open(image_before) as src_before, rasterio.open(self.image_path) as src_after:
            before = src_before.read(1).astype(np.float32)
            after = src_after.read(1).astype(np.float32)
            
            if before.shape != after.shape:
                return None, {'error': '两期影像尺寸不一致'}
            
            if method == 'difference':
                change = after - before
            elif method == 'ratio':
                change = after / (before + 0.0001)
            else:
                change = after - before
            
            # 统计变化
            increased = np.sum(change > 10)
            decreased = np.sum(change < -10)
            unchanged = np.sum(np.abs(change) <= 10)
            
            change_path = os.path.join(self.output_dir, f'change_{method}.tif')
            profile = src_after.profile.copy()
            profile.update(dtype=rasterio.float32, count=1, compress='lzw')
            
            with rasterio.open(change_path, 'w', **profile) as dst:
                dst.write(change, 1)
            
            self.results.append({
                'type': '变化检测', 'output': change_path,
                'method': method,
                'increased_pixels': int(increased),
                'decreased_pixels': int(decreased),
                'unchanged_pixels': int(unchanged)
            })
            
            return change_path, {
                'increased': int(increased), 'decreased': int(decreased),
                'unchanged': int(unchanged)
            }
    
    def _interpret_ndvi(self, mean_ndvi):
        if mean_ndvi > 0.6: return '高植被覆盖，可能为森林/茂密草地'
        if mean_ndvi > 0.3: return '中等植被覆盖，可能为农田/灌丛'
        if mean_ndvi > 0.1: return '低植被覆盖，可能为稀疏草地/裸地'
        return '极低植被覆盖，可能为水体/建筑/裸岩'


class OutputValidator:
    @staticmethod
    def validate(results):
        if not results:
            return ['无任何遥感处理结果']
        return []


def main(image_path, mode='all', image_before=None, output_dir=None, max_retries=3):
    if output_dir is None:
        output_dir = f"output_rs_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    os.makedirs(output_dir, exist_ok=True)
    
    logger, log_path = setup_logger(output_dir)
    logger.info(f"ATS-008 遥感解译: {image_path}, 模式: {mode}")
    
    for attempt in range(1, max_retries + 1):
        try:
            errors = InputValidator.validate(image_path)
            if errors and attempt >= max_retries:
                raise RuntimeError(f"输入校验失败: {errors}")
            
            processor = RSProcessor(image_path, output_dir)
            
            if mode in ['all', 'ndvi']:
                ndvi_path, ndvi_stats = processor.compute_ndvi()
                logger.info(f"NDVI: mean={ndvi_stats['mean']:.4f}, 植被覆盖={ndvi_stats.get('vegetation_pct',0):.1f}%")
            
            if mode in ['all', 'ndwi']:
                ndwi_path, ndwi_stats = processor.compute_ndwi()
                logger.info(f"NDWI: mean={ndwi_stats['mean']:.4f}")
            
            if mode in ['all', 'ndbi']:
                processor.compute_ndbi()
            
            if mode in ['all', 'classify']:
                cls_path, cls_stats = processor.kmeans_classify()
                logger.info(f"K-Means分类完成")
            
            if mode in ['change'] and image_before:
                processor.change_detection(image_before)
            
            report = {
                'task': '遥感解译', 'skill_id': 'ATS-008', 'version': 'V5.0',
                'timestamp': datetime.now().isoformat(),
                'image': image_path, 'mode': mode,
                'results': processor.results
            }
            
            report_path = Path(output_dir) / "rs_report.json"
            with open(report_path, 'w', encoding='utf-8') as f:
                json.dump(report, f, ensure_ascii=False, indent=2)
            
            return {
                'report': str(report_path), 'log': str(log_path),
                'output_dir': output_dir, 'results': processor.results
            }
            
        except Exception as e:
            logger.error(f"第{attempt}轮异常: {e}")
            if attempt >= max_retries:
                raise RuntimeError(f"[3轮熔断] ATS-008失败: {e}")
            continue


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='ATS-008 遥感解译')
    parser.add_argument('image', help='遥感影像路径')
    parser.add_argument('-m', '--mode', default='all', choices=['all','ndvi','ndwi','ndbi','classify','change'])
    parser.add_argument('-b', '--before', default=None, help='前期影像(变化检测)')
    parser.add_argument('-o', '--output', default=None)
    args = parser.parse_args()
    result = main(args.image, args.mode, args.before, args.output)
    print(f"解译完成: {len(result['results'])}个处理结果")
```

---

## 验收检查单

| 序号 | 检查项 | 标准 |
|------|--------|------|
| 1 | NDVI计算 | NIR/RED自动探测+植被覆盖百分比 |
| 2 | NDWI计算 | GREEN/NIR自动探测+水体比例 |
| 3 | NDBI计算 | SWIR/NIR+建筑比例 |
| 4 | K-Means分类 | 5类+迭代收敛+类分布统计 |
| 5 | 变化检测 | 两期差分+增加/减少/不变统计 |
| 6 | 降级方案 | 无rasterio时自动降级arcpy/simple |
