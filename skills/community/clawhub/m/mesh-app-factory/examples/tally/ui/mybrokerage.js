const MINUTE_MS=60000;

export default {
inject:['service', 'tags'],
data() {return {
    list:[], //佣金列表
    range:{from:'',to:''},
    ctrl:{cur:1,max:0},
    score:{total:0,brokerage:0},
}},
created(){
    var dt=new Date();
    var cur=parseInt(dt.getTime()/MINUTE_MS);
    dt.setTime(cur*MINUTE_MS);
    this.range.to=date2str(dt);
    dt.setTime((cur-1440*6)*MINUTE_MS);
    this.range.from=date2str(dt);
    
    this.query(1);
},
methods:{
query(pg) {
    var to=parseInt(new Date(this.range.to).getTime()/MINUTE_MS);
    var from=parseInt(new Date(this.range.from).getTime()/MINUTE_MS);
    var offset=(parseInt(pg)-1)*this.service.NUM_PER_PAGE;
    var url="/report/myBrokerage?offset="+offset
        +"&num="+this.service.NUM_PER_PAGE
        +"&from="+from+"&to="+to;
    request({method:"GET",url:url}, this.service.name).then(resp=>{
        if(resp.code!=RetCode.OK) {
            this.list=[];
            this.ctrl.max=0;
        } else {
            this.score.total=resp.data.total;
            this.score.brokerage=resp.data.brokerage;
            this.list=this.formatData(resp.data.list,resp.data.cols);
            this.ctrl.max=Math.ceil(resp.data.total/this.service.NUM_PER_PAGE);
        }
    })
},
dateChanged() {
    this.ctrl.cur=1;
    this.query(1);
},
formatData(rows,cols) {
    var dt=new Date();
    var bts=this.tags.brokerage.types;
    return rows.map(l=>{
        var r={};
        for(var i in cols) {
            r[cols[i]]=l[i];
        }
        dt.setTime(r.createAt*MINUTE_MS);
        r.createAt=datetime2str(dt);
        r.ratio=this.service.formatNum(r.ratio*100,1);
        r.type=bts[r.type];
        return r;
    })
}
},

template:`
<q-layout view="hHh lpr fFf">
  <q-header class="bg-grey-1 text-primary">
   <q-toolbar>
    <q-btn flat round icon="arrow_back" dense @click="service.back"></q-btn>
    <q-toolbar-title>{{tags.brokerage.title}}</q-toolbar-title>
    <q-btn icon="event" flat dense>
     <q-popup-proxy cover transition-show="scale" transition-hide="scale">
      <q-date v-model="range" range>
       <div class="row items-center justify-end">
        <q-btn :label="tags.ok" color="primary" @click="dateChanged" v-close-popup></q-btn>
        <q-btn :label="tags.close" color="primary" flat v-close-popup></q-btn>
       </div>
      </q-date>
     </q-popup-proxy>
     {{range.from}} => {{range.to}}
    </q-btn>
   </q-toolbar>
   <q-card class="q-mx-sm" flat>
    <q-card-action>
    <q-markup-table flat dark style="background:radial-gradient(circle,#33a2ff 0%,#014aaa 100%)">
     <tr>
      <th>{{tags.score.total}}</th>
      <th>{{tags.score.vTotal}}</th>
     </tr>
     <tr>
      <td class="text-h6 text-center">{{score.total}}</td>
      <td class="text-h6 text-center">{{score.brokerage}}</td>
     </tr>
    </q-markup-table>
    </q-card-section>
   </q-card>
  </q-header>

  <q-page-container>
    <q-page class="q-pa-md">

<div class="q-pa-lg flex flex-center" v-if="ctrl.max>1">
 <q-pagination v-model="ctrl.cur" color="primary" :max="ctrl.max" max-pages="10"
  boundary-numbers="false" @update:model-value="query"></q-pagination>
</div>
<q-markup-table flat>
 <thead><tr>
  <th class="text-left">{{tags.createAt}}</th>
  <th class="text-right">{{tags.brokerage.val}}</th>
  <th class="text-right">{{tags.brokerage.ratio}}</th>
 </tr></thead>
 <tbody>
   <tr v-for="v in list">
    <td class="text-left">{{v.createAt}}</td>
    <td class="text-right">{{v.brokerage}}</td>
    <td class="text-right">{{v.type}} {{v.ratio}}</td>
   </tr>
 </tbody>
</q-markup-table>
    </q-page>
  </q-page-container>
</q-layout>
`
}