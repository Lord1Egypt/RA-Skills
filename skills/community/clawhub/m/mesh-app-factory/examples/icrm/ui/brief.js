export default {
inject:['service', 'tags'],
data() {return {
    beginTime:0,
    days:7,
    mainCharts:null,
    date:'',
    dateStr:''
}},
created(){
    var dt=new Date();
    this.beginTime=Math.ceil(dt.getTime()/86400000)-7;
    this.dateStr=new Date(this.beginTime*86400000).toLocaleDateString()+' - '+dt.toLocaleDateString();
},
mounted(){
    this.mainCharts=Vue.markRaw(echarts.init(document.getElementById('mainCharts')));
    this.query_main();
},
methods:{
query_main() {
    var url="/api/report/main?beginTime="+this.beginTime+"&days="+this.days;
    request({method:"GET",url:url},this.service.name).then(resp => {
        var customer=[], contact=[], ord=[], service=[],
         contract=[], revenue=[], cost=[];
        //var payment=[];
        var xAxis=[];
        var dt=new Date();
        var i, t=this.beginTime*86400000;

        for(i=0;i<this.days;i++){
            customer.push(0);
            contact.push(0);
            ord.push(0);
            service.push(0);
            //payment.push(0);
            contract.push(0);
            revenue.push(0);
            cost.push(0);
            dt.setTime(t);
            t+=86400000;
            if(i==0||dt.getDate()==1){
                xAxis.push(dt.getFullYear()+'-'+(dt.getMonth()+1)+'-'+dt.getDate());
            } else {
                xAxis.push((dt.getMonth()+1)+'-'+dt.getDate());
            }
        }
        if(resp.code==RetCode.OK) {
            t=this.beginTime;
            //customer,contact,ord,service,payment,contract,revenue,cost,reportAt
            resp.data.data.forEach(l => {
                i=l[0]-t;
                customer[i]=l[1];
                contact[i]=l[2];
                ord[i]=l[3];
                service[i]=l[4];
                //payment[i]=l[5];
                contract[i]=l[6];
                revenue[i]=l[7];
                cost[i]=l[8];
            });
        }
        var series=[
            {name:this.tags.report.customer,type:'line',data:customer,yAxisIndex:0},
            {name:this.tags.report.contact,type:'line',data:contact,yAxisIndex:0},
            {name:this.tags.report.ord,type:'line',data:ord,yAxisIndex:0},
            {name:this.tags.report.service,type:'line',data:service,yAxisIndex:0},
            //{name:this.tags.report.payment,type:'bar',data:payment,yAxisIndex:0,stack:"flow"},
            {name:this.tags.report.contract,type:'bar',data:contract,yAxisIndex:1,stack:"flow"},
            {name:this.tags.report.revenue,type:'bar',data:revenue,yAxisIndex:1,stack:"balance"},
            {name:this.tags.report.cost,type:'bar',data:cost,yAxisIndex:1,stack:"balance"}
        ];
        
        this.mainCharts.setOption({
            title: {show:false},
            tooltip: {},
            legend: {type:'scroll',bottom:10,width:this.service.CLIENTW-60},
            grid: {left:'0%',containLabel:true},
            xAxis: {data:xAxis,type: 'category'},
            yAxis: [{name:this.tags.unit.g,minInterval:1},{name:this.tags.unit.y}],
            series: series
        });
    })
},
date_range_end(range) {
    var f=range.from;
    var t=range.to;
    var ft=new Date(f.year,f.month-1,f.day);
    var tt=new Date(t.year,t.month-1,t.day);
    this.dateStr=ft.toLocaleDateString()+' - '+tt.toLocaleDateString();
    this.beginTime=Math.ceil(ft.getTime()/86400000);
    this.days=Math.ceil(tt.getTime()/86400000)-this.beginTime+1;
    if(this.days<=31) {
        this.query_main();
    } else {
        this.$refs.errMsg.show(this.tags.exceedsDayNum);
    }
}
},

template:`
<q-layout view="hHh lpr fFf">
<q-header>
 <q-toolbar>
  <q-btn flat round icon="arrow_back" dense @click="service.back"></q-btn>
  <q-toolbar-title>{{tags.home.bulletin}}</q-toolbar-title>
 </q-toolbar>
</q-header>
<q-footer class="bg-white text-primary q-pa-md">
<q-input v-model="dateStr">
 <template v-slot:prepend>
  <q-icon name="event" class="cursor-pointer">
  <q-popup-proxy transition-show="scale" transition-hide="scale">
    <q-date v-model="date" range @range-end="date_range_end" minimal>
      <div class="row items-center justify-end">
        <q-btn v-close-popup :label="tags.close" color="primary" flat></q-btn>
      </div>
    </q-date>
  </q-popup-proxy>
  </q-icon>
 </template>
</q-input>
</q-footer>

<q-page-container>
 <q-page class="q-pa-sm">
<div id="mainCharts" :style="{width:'100vw', height:'70vh'}"></div>
 </q-page>
</q-page-container>
</q-layout>
<component-alert-dialog :title="tags.failToCall" :errMsgs="tags.errMsgs" :close="tags.close" ref="errMsg"></component-alert-dialog>
`
}