# MATLAB Bridge - 常用代码模板库
# 快速生成常用MATLAB代码片段

class MATLABTemplates:
    """MATLAB常用代码模板"""
    
    @staticmethod
    def plot_time_series(t, y, title="Time Series", xlabel="Time (s)", ylabel="Amplitude"):
        """生成时程曲线绘图代码"""
        code = f"""
% 绘制时程曲线
figure('Position', [100 100 800 400]);
plot({t}, {y}, 'LineWidth', 1.2);
title('{title}');
xlabel('{xlabel}');
ylabel('{ylabel}');
grid on;
set(gca, 'FontSize', 12);
% 保存图片
saveas(gcf, 'time_series.png');
print(gcf, 'time_series', '-dpdf', '-r300');
disp('Plot saved: time_series.png and time_series.pdf');
"""
        return code.strip()
    
    @staticmethod
    def fft_analysis(signal, fs):
        """FFT频谱分析代码"""
        code = f"""
% FFT频谱分析
N = length({signal});
Y = fft({signal});
P2 = abs(Y/N);
P1 = P2(1:N/2+1);
P1(2:end-1) = 2*P1(2:end-1);
f = {fs}*(0:(N/2))/N;

% 绘制频谱
figure('Position', [100 100 800 400]);
plot(f, P1, 'LineWidth', 1.2);
title('Single-Sided Amplitude Spectrum');
xlabel('Frequency (Hz)');
ylabel('|P1(f)|');
grid on;
set(gca, 'FontSize', 12);
% 保存
saveas(gcf, 'fft_spectrum.png');
print(gcf, 'fft_spectrum', '-dpdf', '-r300');
disp('FFT analysis complete');
"""
        return code.strip()
    
    @staticmethod
    def response_spectrum(acc, dt, zeta=0.05, Tn=None):
        """生成反应谱计算代码"""
        if Tn is None:
            Tn = "logspace(-2, 1, 100)"  # 0.01s到10s
        
        code = f"""
% 计算反应谱
Tn = {Tn};  % 周期范围
zeta = {zeta};  % 阻尼比
dt = {dt};  % 时间步长
acc = {acc};  % 加速度时程

Sa = zeros(size(Tn));
for i = 1:length(Tn)
    omega = 2*pi/Tn(i);
    wd = omega*sqrt(1-zeta^2);
    
    % Newmark-beta方法计算响应
    % (简化实现)
    u = 0; v = 0; a = -acc(1);
    umax = 0;
    
    for j = 2:length(acc)
        % 简化计算
        a_new = -acc(j) - 2*zeta*omega*v - omega^2*u;
        v = v + dt/2*(a + a_new);
        u = u + dt*v;
        a = a_new;
        umax = max(umax, abs(u));
    end
    
    Sa(i) = omega^2*umax;
end

% 绘制反应谱
figure('Position', [100 100 600 400]);
semilogx(Tn, Sa/9.8, 'LineWidth', 1.5);  % 转换为g
title('Response Spectrum');
xlabel('Period (s)');
ylabel('Sa (g)');
grid on;
set(gca, 'FontSize', 12);
% 保存
saveas(gcf, 'response_spectrum.png');
print(gcf, 'response_spectrum', '-dpdf', '-r300');
disp('Response spectrum calculation complete');
"""
        return code.strip()
    
    @staticmethod
    def filter_signal(signal, fs, ftype, fc):
        """信号滤波代码"""
        code = f"""
% 设计滤波器
fs = {fs};  % 采样频率
fc = {fc};  % 截止频率

if strcmp('{ftype}', 'low')
    [b, a] = butter(4, fc/(fs/2), 'low');
elif strcmp('{ftype}', 'high')
    [b, a] = butter(4, fc/(fs/2), 'high');
elif strcmp('{ftype}', 'band')
    [b, a] = butter(4, fc/(fs/2), 'bandpass');
end

% 滤波
{signal}_filtered = filtfilt(b, a, {signal});

% 对比图
figure('Position', [100 100 1000 400]);
subplot(1,2,1);
plot({signal}, 'LineWidth', 1);
title('Original Signal');
grid on;
subplot(1,2,2);
plot({signal}_filtered, 'LineWidth', 1);
title('Filtered Signal');
grid on;
% 保存
saveas(gcf, 'filter_comparison.png');
print(gcf, 'filter_comparison', '-dpdf', '-r300');
disp('Filtering complete');
"""
        return code.strip()
    
    @staticmethod
    def plot_hysteresis(disp, force, title="Hysteresis Curve"):
        """滞回曲线绘图"""
        code = f"""
% 绘制滞回曲线
figure('Position', [100 100 600 600]);
plot({disp}, {force}, 'LineWidth', 1.2);
title('{title}');
xlabel('Displacement');
ylabel('Force');
grid on;
axis equal;
set(gca, 'FontSize', 12);
% 保存
saveas(gcf, 'hysteresis.png');
print(gcf, 'hysteresis', '-dpdf', '-r300');
disp('Hysteresis curve saved');
"""
        return code.strip()
    
    @staticmethod
    def batch_process_csv(file_pattern, operation):
        """批量处理CSV文件"""
        code = f"""
% 批量处理CSV文件
files = dir('{file_pattern}');
results = struct();

for i = 1:length(files)
    filename = files(i).name;
    filepath = fullfile(files(i).folder, filename);
    
    % 读取数据
    data = readmatrix(filepath);
    
    % 执行操作: {operation}
    result_{operation} = data;  % 这里根据实际操作修改
    
    % 保存结果
    [~, name, ~] = fileparts(filename);
    output_name = sprintf('%s_processed.csv', name);
    writematrix(result_{operation}, output_name);
    
    fprintf('Processed: %s -> %s\\n', filename, output_name);
end

disp('Batch processing complete');
"""
        return code.strip()


# 快捷函数
def quick_plot(y, t=None, title="Plot"):
    """快速生成绘图代码"""
    if t is None:
        t = "1:length(y)"
    return MATLABTemplates.plot_time_series(t, 'y', title)


def quick_fft(signal, fs):
    """快速生成FFT代码"""
    return MATLABTemplates.fft_analysis('signal', fs)


def quick_spectrum(acc, dt):
    """快速生成反应谱代码"""
    return MATLABTemplates.response_spectrum('acc', dt)
