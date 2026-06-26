import {
  AbsoluteFill,
  Sequence,
  useVideoConfig,
  useCurrentFrame,
  interpolate,
  spring,
  Easing,
} from "remotion";
import { FadeIn } from "../components/FadeIn";
import { SlideIn } from "../components/SlideIn";

/**
 * 数据项接口
 */
interface DataItem {
  label: string;
  value: number;
  color?: string;
}

/**
 * 图表数据
 */
const chartData: DataItem[] = [
  { label: "Q1", value: 65, color: "#667eea" },
  { label: "Q2", value: 85, color: "#764ba2" },
  { label: "Q3", value: 75, color: "#f093fb" },
  { label: "Q4", value: 95, color: "#f5576c" },
];

/**
 * 统计数据
 */
const statsData = [
  { label: "Users", value: "10M+", icon: "👥" },
  { label: "Revenue", value: "$50M", icon: "💰" },
  { label: "Growth", value: "150%", icon: "📈" },
];

/**
 * 柱状图组件
 */
const BarChart: React.FC<{ data: DataItem[]; startFrame: number }> = ({
  data,
  startFrame,
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const barWidth = 120;
  const barGap = 40;
  const maxHeight = 400;
  const totalWidth = data.length * barWidth + (data.length - 1) * barGap;

  return (
    <div
      style={{
        display: "flex",
        alignItems: "flex-end",
        justifyContent: "center",
        gap: barGap,
        height: maxHeight,
      }}
    >
      {data.map((item, index) => {
        const delay = startFrame + index * 10;
        const progress = spring({
          frame: frame - delay,
          fps,
          config: { damping: 15, stiffness: 80 },
        });

        const barHeight = item.value / 100 * maxHeight * progress;

        return (
          <div
            key={item.label}
            style={{
              display: "flex",
              flexDirection: "column",
              alignItems: "center",
            }}
          >
            {/* 数值标签 */}
            <div
              style={{
                marginBottom: 10,
                fontSize: 28,
                color: "#ffffff",
                fontFamily: "Arial, sans-serif",
                fontWeight: "bold",
                opacity: progress,
              }}
            >
              {item.value}%
            </div>

            {/* 柱子 */}
            <div
              style={{
                width: barWidth,
                height: barHeight,
                backgroundColor: item.color,
                borderRadius: "10px 10px 0 0",
                boxShadow: `0 0 20px ${item.color}50`,
                transition: "height 0.3s ease",
              }}
            />

            {/* 标签 */}
            <div
              style={{
                marginTop: 15,
                fontSize: 24,
                color: "#888888",
                fontFamily: "Arial, sans-serif",
              }}
            >
              {item.label}
            </div>
          </div>
        );
      })}
    </div>
  );
};

/**
 * 环形图组件
 */
const DonutChart: React.FC<{ data: DataItem[]; startFrame: number }> = ({
  data,
  startFrame,
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const progress = spring({
    frame: frame - startFrame,
    fps,
    config: { damping: 20, stiffness: 50 },
  });

  const size = 300;
  const strokeWidth = 40;
  const radius = (size - strokeWidth) / 2;
  const circumference = 2 * Math.PI * radius;
  const center = size / 2;

  // 计算每个段的起止角度
  const total = data.reduce((sum, item) => sum + item.value, 0);
  let currentAngle = -90; // 从顶部开始

  return (
    <div style={{ position: "relative", width: size, height: size }}>
      <svg width={size} height={size}>
        {/* 背景圆环 */}
        <circle
          cx={center}
          cy={center}
          r={radius}
          fill="none"
          stroke="#333"
          strokeWidth={strokeWidth}
        />

        {/* 数据段 */}
        {data.map((item, index) => {
          const percentage = item.value / total;
          const strokeDasharray = circumference * percentage * progress;
          const strokeDashoffset = circumference * (1 - percentage * progress);

          const dashArray = `${strokeDasharray} ${circumference}`;
          const dashOffset =
            -circumference * ((currentAngle + 90) / 360) * progress;

          currentAngle += percentage * 360;

          return (
            <circle
              key={item.label}
              cx={center}
              cy={center}
              r={radius}
              fill="none"
              stroke={item.color}
              strokeWidth={strokeWidth}
              strokeDasharray={dashArray}
              strokeDashoffset={dashOffset}
              style={{
                transform: `rotate(${currentAngle - percentage * 360 - 90}deg)`,
                transformOrigin: `${center}px ${center}px`,
              }}
            />
          );
        })}
      </svg>

      {/* 中心文字 */}
      <div
        style={{
          position: "absolute",
          top: "50%",
          left: "50%",
          transform: "translate(-50%, -50%)",
          textAlign: "center",
        }}
      >
        <div style={{ fontSize: 48, color: "#ffffff", fontWeight: "bold" }}>
          {Math.round(total * progress)}
        </div>
        <div style={{ fontSize: 20, color: "#888888" }}>Total</div>
      </div>
    </div>
  );
};

/**
 * 统计卡片组件
 */
const StatCard: React.FC<{
  label: string;
  value: string;
  icon: string;
  index: number;
  startFrame: number;
}> = ({ label, value, icon, index, startFrame }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const delay = startFrame + index * 10;
  const progress = spring({
    frame: frame - delay,
    fps,
    config: { damping: 15, stiffness: 100 },
  });

  return (
    <div
      style={{
        width: 280,
        padding: "30px 40px",
        backgroundColor: "rgba(255,255,255,0.05)",
        borderRadius: 20,
        textAlign: "center",
        transform: `scale(${progress})`,
        opacity: progress,
        border: "1px solid rgba(255,255,255,0.1)",
      }}
    >
      <div style={{ fontSize: 60, marginBottom: 15 }}>{icon}</div>
      <div
        style={{
          fontSize: 48,
          color: "#667eea",
          fontFamily: "Arial, sans-serif",
          fontWeight: "bold",
          marginBottom: 10,
        }}
      >
        {value}
      </div>
      <div
        style={{
          fontSize: 24,
          color: "#888888",
          fontFamily: "Arial, sans-serif",
        }}
      >
        {label}
      </div>
    </div>
  );
};

/**
 * 图表标题场景
 */
const ChartTitleScene: React.FC<{ title: string }> = ({ title }) => {
  return (
    <AbsoluteFill
      style={{
        backgroundColor: "#0a0a0a",
        justifyContent: "center",
        alignItems: "center",
      }}
    >
      <FadeIn duration={20}>
        <h1
          style={{
            fontSize: 80,
            color: "#ffffff",
            fontFamily: "Arial, sans-serif",
            margin: 0,
          }}
        >
          {title}
        </h1>
      </FadeIn>
    </AbsoluteFill>
  );
};

/**
 * 柱状图场景
 */
const BarChartScene: React.FC = () => {
  return (
    <AbsoluteFill
      style={{
        backgroundColor: "#0a0a0a",
        justifyContent: "center",
        alignItems: "center",
        padding: 60,
      }}
    >
      <SlideIn direction="top" duration={20}>
        <h2
          style={{
            fontSize: 50,
            color: "#ffffff",
            fontFamily: "Arial, sans-serif",
            margin: "0 0 60px",
            textAlign: "center",
          }}
        >
          Quarterly Performance
        </h2>
      </SlideIn>
      <BarChart data={chartData} startFrame={20} />
    </AbsoluteFill>
  );
};

/**
 * 环形图场景
 */
const DonutChartScene: React.FC = () => {
  return (
    <AbsoluteFill
      style={{
        backgroundColor: "#0a0a0a",
        justifyContent: "center",
        alignItems: "center",
      }}
    >
      <SlideIn direction="top" duration={20}>
        <h2
          style={{
            fontSize: 50,
            color: "#ffffff",
            fontFamily: "Arial, sans-serif",
            margin: "0 0 60px",
            textAlign: "center",
          }}
        >
          Market Distribution
        </h2>
      </SlideIn>
      <DonutChart data={chartData} startFrame={20} />
    </AbsoluteFill>
  );
};

/**
 * 统计数据场景
 */
const StatsScene: React.FC = () => {
  return (
    <AbsoluteFill
      style={{
        backgroundColor: "#0a0a0a",
        justifyContent: "center",
        alignItems: "center",
      }}
    >
      <SlideIn direction="top" duration={20}>
        <h2
          style={{
            fontSize: 50,
            color: "#ffffff",
            fontFamily: "Arial, sans-serif",
            margin: "0 0 60px",
            textAlign: "center",
          }}
        >
          Key Metrics
        </h2>
      </SlideIn>
      <div style={{ display: "flex", gap: 40 }}>
        {statsData.map((stat, index) => (
          <StatCard
            key={stat.label}
            label={stat.label}
            value={stat.value}
            icon={stat.icon}
            index={index}
            startFrame={20}
          />
        ))}
      </div>
    </AbsoluteFill>
  );
};

/**
 * DataVisualization - 数据展示模板
 *
 * 提供多种数据可视化动画效果：
 * - 柱状图动画
 * - 环形图动画
 * - 统计卡片动画
 */
export const DataVisualization: React.FC = () => {
  const { fps } = useVideoConfig();

  const sceneDuration = 4;
  const sceneFrames = sceneDuration * fps;

  return (
    <AbsoluteFill>
      {/* 场景1: 标题 */}
      <Sequence from={0} durationInFrames={sceneFrames}>
        <ChartTitleScene title="Data Insights" />
      </Sequence>

      {/* 场景2: 柱状图 */}
      <Sequence from={sceneFrames} durationInFrames={sceneFrames}>
        <BarChartScene />
      </Sequence>

      {/* 场景3: 环形图 */}
      <Sequence from={sceneFrames * 2} durationInFrames={sceneFrames}>
        <DonutChartScene />
      </Sequence>

      {/* 场景4: 统计数据 */}
      <Sequence from={sceneFrames * 3} durationInFrames={sceneFrames}>
        <StatsScene />
      </Sequence>
    </AbsoluteFill>
  );
};

export default DataVisualization;
