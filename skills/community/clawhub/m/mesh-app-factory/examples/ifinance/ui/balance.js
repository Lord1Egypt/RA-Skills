export default {
inject:['tags','service'],
data() {return {
    balCharts:null,
    bals:[],
    type:{dlg:false,chged:false,list:[],labels:{}},
    ctrl:{month:{year:0,month:1},monNum:12},
    chart:{x:[],series:[]}
}},
created(){
    //将labels扁平化，便于模板中显示
    var types=storageGet('balance_types','["CUR_CASH","CUR_RECV","CDEBT_NEEDPAY","CDEBT_SALARY"]');
    this.type.list=JSON.parse(types);
    var labels={};
    for(var cls in this.tags.balTypes) {
        labels=Object.assign(labels, this.tags.balTypes[cls].types);
    }
    this.type.labels=labels;
},
mounted(){ //mounted在created之后
    this.balCharts=Vue.markRaw(echarts.init(document.getElementById('balCharts')));
},
methods:{
query() {
    var end=this.ctrl.month.num;
    var start=end-this.ctrl.monNum;
    var dta={start:start, end:end, types:this.type.list};
    request({method:"POST",url:"/balance/snapshot",data:dta},this.service.name).then(resp=>{
        if(resp.code!=RetCode.OK) {
            resp.data={list:[]}
        }
        var m,sm;
        var monNum=this.ctrl.monNum;
        var bals=new Array(monNum); //按月分行，每行记录多个类型
        var xAxis=[];
        var bal;
        for(var i=0;i<monNum;i++) {
            m=i+start+1;
            sm=parseInt(m/12)+'/'+((m%12)+1);
            bal={month:sm};
            for(var type in this.type.list) bal[type]=0;
            bals[monNum-i-1]=bal; //倒序
            xAxis.push(sm);
        }
        this.chart.x=xAxis;

        var bals1={}; //按类型分行，每行n个月
        for(var type of this.type.list) {//每个类型填充n个0
            bals1[type]=new Array(monNum).fill(0);;
        }

        var v;
        resp.data.list.map(l => { //向bals中填充实际值，没有的保持0值
            m=l.month-start-1;
            v=l.val.toFixed(2);
            bals[monNum-m-1][l.type]=v; //倒序
            bals1[l.type][m]=v;
        })
        this.bals=bals;
        
        var series=[];
        for(var type in bals1) {
            series.push({name:this.type.labels[type],type:'line',data:bals1[type]});
        }
        this.chart.series=series;
        this.show_chart();
    })
},
show_chart() {
    this.balCharts.clear();//没有clear，减少series后，不会更新
    this.balCharts.setOption({
        title: {show:false},
        tooltip: {},
        grid: {left:'0%',containLabel:true},
        legend: {type:'scroll',bottom:10,width:this.service.CLIENTW-60},
        xAxis: {data:this.chart.x},
        yAxis: [{name:this.tags.balance.val}],
        series: this.chart.series
    });
},
set_types() {
    if(this.type.chged) {
        var types=this.type.list.filter(tp=>{
            return this.type.labels[tp];
        })
        this.type.list=types;
        storageSet('balance_types', JSON.stringify(types));
        this.type.chged=false;
        this.query();
    }
}
},
template:`
<q-layout view="hHh lpr fFf">
  <q-header>
   <q-toolbar>
    <q-btn flat icon="arrow_back" dense @click="service.back"></q-btn>
    <q-toolbar-title>{{tags.balance.title}}</q-toolbar-title>
    <q-btn flat icon="list" dense @click="type.dlg=true"></q-btn>
    <month-input class="text-subtitle1 q-pl-sm" v-model="ctrl.month"
     @update:modelValue="query" min="-10y" max="cur"></month-input>
   </q-toolbar>
  </q-header>
  <q-page-container>
    <q-page class="q-pa-md">
<div id="balCharts" :style="{width:'99vw', height:'45vh'}"></div>
<q-markup-table flat dense>
  <thead>
    <tr>
     <th>
      <q-btn flat icon="playlist_add" dense color="primary"
      @click="service.goto('/balancelog')"></q-btn>
     </th>
     <th v-for="i in type.list">{{type.labels[i]}}</th>
    </tr>
   </thead>
   <tbody>
     <tr v-for="(l,m) in bals">
      <td class="text-left">{{l.month}}</td>
      <td class="text-center" v-for="i in type.list">{{l[i]}}</td>
     </tr>
   </tbody>
</q-markup-table>
    </q-page>
  </q-page-container>
</q-layout>

<q-dialog v-model="type.dlg" position="top" @hide="set_types">
 <q-card style="width:100vw">
  <q-card-section>
   <div v-for="bt in tags.balTypes">
    <div>{{bt.label}}</div>
    <div class="q-gutter-sm">
     <q-checkbox v-for="(l,tp) in bt.types" @update:model-value="type.chged=true"
      v-model="type.list" :val="tp" :label="l"></q-checkbox>
    </div>
   </div>
  </q-card-section>
 </q-card>
</q-dialog>

<alert-dialog :title="tags.failToCall" :errMsgs="tags.errMsgs" ref="alertDlg"></alert-dialog>
`
}